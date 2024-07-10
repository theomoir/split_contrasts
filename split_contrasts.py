#!/usr/bin/env python3
import csv
import argparse

def splitContrast(samplesHandle, contrastsHandle, outputHandle):
    '''Void function that creates files at the outputHandle based on the contents of
       a file of listed contrasts, and a file of samples (experiments).
       Parameters
       ----------
            samplesHandle(string) : The location of the sample file
            contrastsHandle(string) : The location of the sample file
            outputHandle(string) : The location of where to output files
       Returns
       -------
            none
    '''
    with open(contrastsHandle, newline='') as conrastCSVFile:
        #find dialect of contrast file
        dialect = csv.Sniffer().sniff(conrastCSVFile.readline())
        conrastCSVFile.seek(0)
        #add reader to it
        contrastReader = csv.DictReader(conrastCSVFile, dialect=dialect)
        header = contrastReader.fieldnames
        #Read through line of each contrast file
        for row in contrastReader:
            rowID = row['id']
            #Create and write contrast file - contrast file is just the current line of row
            #but inside of an array
            WriteCSVFile(f'{outputHandle}/contrast__{rowID}.csv', [row])
            #Create and write a corresponding sample file 
            sampleRows = GenerateSampleFile(samplesHandle, header, row)
            WriteCSVFile(f'{outputHandle}/sample__{rowID}.csv', sampleRows)


def WriteCSVFile(outputHandle, lines):
    '''Creates a two line contrast file at outputHandle, signifying one contrast.
       Parameters
       ----------
            outputHandle (string) : Location of where to create file
            line (list of dictionaries) : The lines to be placed in the body of the file
       Returns
       -------
            none'''
    #First get the header of the file - also known as the keys of the dictionary
    header = list(lines[0].keys())
    #Then simply write them to a file
    with open(outputHandle, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(lines)



def GenerateSampleFile(samplesHandle, contrastHeader, line):
    '''Creates a list of dictionaries representing the sample file , containing the valid 
       experiments specified in the corresponding contrast file.
       Parameters
       ----------
            samplesHandle (string) : The location of the file containing all samples (experiments)
            contrastHeader (string) : The header of the latter mentioned sample file
            line (string) : Also from the sample file, specifies what samples (experiments)
                are to be ignored
       Returns
       -------
            OutputListOfDict (list of dictionaries): Returns a list of dictionaries containing a 
            sample sheet'''
    with open(samplesHandle, newline='') as sampleCSVFile:
        #find dialect of sample file
        dialect = csv.Sniffer().sniff(sampleCSVFile.readline())
        sampleCSVFile.seek(0)
        #add reader to it
        sampleReader = csv.DictReader(sampleCSVFile, dialect=dialect)
        #Check if exclusion is a paramter, and if so are there any associated values to exclude
        if ('exclude_samples_col' in contrastHeader and 'exclude_samples_values' in contrastHeader and line['exclude_samples_values'] != ''):
            #the column to remove from, values to remove
            excludeSampleCol, excludeSampleValue = line['exclude_samples_col'], line['exclude_samples_values']
            #finds the delimiter of the excludedSampleValue (this can be removed if it is
            #always known to be a semicolon)
            ExclDialect = csv.Sniffer().sniff(excludeSampleValue)
            #creates set with unwanted class values
            excludedArray = set(excludeSampleValue.split(ExclDialect.delimiter))
            #go through each row, checking if it contains any excluded classes, and if not appending it to OutputListodDict
            OutputListOfDict = [row for row in sampleReader if row[excludeSampleCol] not in excludedArray]
            return OutputListOfDict
        else:
            #if there is nothing to remove, then it simply turns the reader into a list
            return list(sampleReader)



parser = argparse.ArgumentParser(prog="split_contrasts",
                                 description="split singular sample file and contrast into seperate contrast and sample locations")
parser.add_argument("--InputSample", "-is", type=str, help="Location of sample file")
parser.add_argument("--InputContrast", "-ic", type=str, help="Location of contrast file")
parser.add_argument("--Output", "-o", type=str, help="File output location")
args = parser.parse_args()

if __name__ == "__main__":
    splitContrast(args.InputSample, args.InputContrast, args.Output)
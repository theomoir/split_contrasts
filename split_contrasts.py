#!/usr/bin/env python3
import csv

import argparse
import logging
import sys

__version__ = "1.0.1"

def error(msg, exit_code=1):
    logging.error(msg)
    sys.exit(exit_code)

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
    try:
        with open(contrastsHandle, newline='') as contrastCSVFile:
            #find dialect of contrast file
            dialect = csv.Sniffer().sniff(contrastCSVFile.readline())
            contrastCSVFile.seek(0)
            logging.debug(f"Contrast file dialect delimiter: {dialect.delimiter} Contrast file dialect skip initial space: {dialect.skipinitialspace}")
            logging.debug(f"Contrast file dialect escapechar: {dialect.escapechar} Contrast file dialect quotechar: {dialect.quotechar}")
            #add reader to it
            contrastReader = csv.DictReader(contrastCSVFile, dialect=dialect)
            header = contrastReader.fieldnames
            #Read through line of each contrast file
            for row in contrastReader:
                try:
                    rowID = row['id']
                    logging.info(f"Creating {rowID} files...")
                except KeyError:
                    error("cvs file does not contain an 'id' column")
                #Create and write contrast file - contrast file is just the current line of row
                #but inside of a list
                WriteCSVFile(f'{outputHandle}/contrast__{rowID}.csv', [row])
                #Create and write a corresponding sample file 
                sampleRows = GenerateSampleFile(samplesHandle, header, row)
                WriteCSVFile(f'{outputHandle}/sample__{rowID}.csv', sampleRows)
            logging.info("Task finished :)")
    except IOError:
        error(f"{contrastsHandle} does not exist")


def WriteCSVFile(outputHandle, CVSdict):
    '''Creates a two line contrast file at outputHandle, signifying one contrast.
       Parameters
       ----------
            outputHandle (string) : Location of where to create file
            CVSdict (list of dictionaries) : The lines to be placed in the body of the file
       Returns
       -------
            none'''
    #First get the header of the file - also known as the keys of the dictionary
    header = list(CVSdict[0].keys())
    #Then simply write them to a file
    try:
        with open(outputHandle, 'w', newline='') as csvfile:
            logging.debug(f"Writing CVS file...")
            writer = csv.DictWriter(csvfile, fieldnames=header)
            writer.writeheader()
            writer.writerows(CVSdict)
    except IOError:
        error(f"{outputHandle} does not exist")
        




def GenerateSampleFile(samplesHandle, contrastHeader, currentSample):
    '''Creates a list of dictionaries representing the sample file , containing the valid 
       experiments specified in the corresponding contrast file.
       Parameters
       ----------
            samplesHandle (string) : The location of the file containing all samples (experiments)
            contrastHeader (string) : The header of the latter mentioned sample file
            currentSample (string) : Also from the sample file, specifies what samples (experiments)
                are to be ignored
       Returns
       -------
            OutputListOfDict (list of dictionaries): Returns a list of dictionaries containing a 
            sample sheet'''
    try:
        with open(samplesHandle, newline='') as sampleCSVFile:
            logging.debug(f"Finding appropriate sample file for {currentSample['id']}")
            #find dialect of sample file
            dialect = csv.Sniffer().sniff(sampleCSVFile.readline())
            sampleCSVFile.seek(0)
            logging.debug(f"Sample file dialect delimiter: {dialect.delimiter} Sample file dialect skip initial space: {dialect.skipinitialspace}")
            logging.debug(f"Sample file dialect escapechar: {dialect.escapechar} Sample file dialect quotechar: {dialect.quotechar}")
            #add reader to it
            sampleReader = csv.DictReader(sampleCSVFile, dialect=dialect)
            #Check if exclusion is a paramter, and if so are there any associated values to exclude
            if ('exclude_samples_col' in contrastHeader and 'exclude_samples_values' in contrastHeader and currentSample['exclude_samples_values'] != ''):
                #the column to remove from, values to remove
                excludeSampleCol, excludeSampleValue = currentSample['exclude_samples_col'], currentSample['exclude_samples_values']
                #finds the delimiter of the excludedSampleValue (this can be removed if it is
                #always known to be a semicolon)
                exclDialect = csv.Sniffer().sniff(excludeSampleValue)
                logging.debug(f'exclude_samples_values delimiter sniffed to be: {exclDialect.delimiter}')
                #creates set with unwanted class values
                excludedArray = set(excludeSampleValue.split(exclDialect.delimiter))
                logging.debug(f"Exclude array delimiter found to be {exclDialect.delimiter}")
                #go through each row, checking if it contains any excluded classes, and if not appending it to OutputListodDict
                outputListOfDict = [row for row in sampleReader if row[excludeSampleCol] not in excludedArray]
                logging.debug(f"Tail of sample file list: {outputListOfDict[-1]}")
                return outputListOfDict
            else:
                #if there is nothing to remove, then it simply turns the reader into a list
                logging.info(f"Input {currentSample['sample']} contains either no 'exlude_samples_col', no 'exlude_samples_values' or 'exlude_samples_col' is empty")
                return list(sampleReader)
    except IOError:
        error(f"{samplesHandle} does not exist")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="split_contrasts",
                                 description="split singular sample file and contrast into seperate contrast and sample locations")
    parser.add_argument(dest="InputSample", metavar="SAMPLE", type=str, help="Location of sample file")
    parser.add_argument(dest="InputContrast", metavar="CONTRAST", type=str, help="Location of contrast file")
    parser.add_argument("--Output", "-o", default='.', metavar="OUTPUT", type=str, help="File output location")

    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-v", "--verbose", dest="verbosity", default="error", choices=["error", "warning", "info", "debug"], help=f"Set logging level (default error)")
    args = parser.parse_args()
    logging.basicConfig(format="%(levelname)s: %(message)s", level=args.verbosity.upper())
    splitContrast(args.InputSample, args.InputContrast, args.Output)
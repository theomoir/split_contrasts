# split_contrasts

### Synopsis
Splits a sample and contrast file into individual contrasts files, each with their own corresponding sample file adjusted for exclude_samples_values (if specified)

### Example Input

<u>Contrast Table</u>
| Contrast id | target | blocking | exclude_samples_col |exclude_samples_values |
| :---------: | :----: | :------: | :-----------------: | :--------------------:|
| a_vs_none   | none   | a        | colour              | red, blue             |
| a_vs_b      | none   | b        | colour              | yellow                |

<u>Sample Table</u>

| Sample id   | link   |  colour  |
| :---------: | :----: |  :-----: |
| sample_1    | http://| red      |
| sample_2    | http://| red      |
| sample_3    | http://| yellow   |
| sample_4    | http://| blue     |

### Example Output

<u>Table One </u>
| Contrast id | target | blocking | exclude_samples_col |exclude_samples_values |
| :---------: | :----: | :------: | :-----------------: | :--------------------:|
| a_vs_none   | none   | a        | colour              | red, blue             |

| Sample id   | link   |  colour  |
| :---------: | :----: |  :-----: |
| sample_3    | http://| yellow   |

<u>Table Two </u>

| Contrast id | target | blocking | exclude_samples_col |exclude_samples_values |
| :---------: | :----: | :------: | :-----------------: | :--------------------:|
| a_vs_b      | none   | b        | colour              | yellow                |

| Sample id   | link   |  colour  |
| :---------: | :----: |  :-----: |
| sample_1    | http://| red      |
| sample_2    | http://| red      |
| sample_4    | http://| blue     |

### Limitations
- Sample and contrast table must be <b>.csv</b> files
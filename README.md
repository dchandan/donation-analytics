## Approach

The solution to the challenge is provided using a number of classes contained in several python files.
These classes are summarized in the table below.

| Class | File | Note |
| :----- | :---- | :----- |
| AnalyticsApp | app.py | Main application |
| Record | record.py | Defines an invidivudal record |
| BadRecord | record.py | An exception class raised when a data string passed to Record class is bad |
| Donors | donors.py | Tree structure to contain info on all donors the program has seen thus far|
| Donations | donations.py | Contains all donations made to a specific committee from a specific zip code and in a specific year |
| RepeatDonations | donations.py | Tree data structure that contains all donations that have been assessed to be repeat donations |


### The `Record` class
The task of parsing a string containing a donation record and checking whether it is acceptable
is performed by this class. It is invoked simply as a constructor and offers no other "public
interface" (insofar as Python's approach to public interface is concerned). If the string is
parsable without errors, and is assessed to be complete with regards to out problem, then a `Record`
class object is created, otherwise an exception of type `BadRecord` is raised.

Henceforth, in this document a "record" will be meant to represent an object of the `Record` class.

### The `Donors` class
The determination of any record as repeat or not invariably requires checking against
the other records that we have been made aware of up to that point. **Therefore, to not adversely
affect program runtime performance over large datasets, it becomes necessary that we store this
information in an efficient manner**.

I accomplish this using a **tree structure**. Given the formulaiton of our problem, we only need to
store three pieces of information from any donation record: the NAME of the donor, the ZIP_CODE
of the donor and the YEAR of the donation.

The tree data structure (shown below) makes looking up for repeat donors very fast. The `Donors` class itself is the
head node and has its children nodes the various ZIP_CODE that we have seen so far (i.e. each
zipcode will be a node). Each
ZIP_CODE node itself has its children nodes corresponding to each donor from that zipcode. Finally, this
lowest level node internally contains a list of all the years that donor has donated.

**Example:** Suppose the following new record comes by:

> **C00384516**|N|M2|P|201702039042410893|15|IND|**SABOURIN, JAMES**|LOOKOUT MOUNTAIN|GA|**028956146**|UNUM|SVP, CORPORATE COMMUNICATIONS|**01312017**|**230**||PR1890575345050|1147350||P/R DEDUCTION ($115.00 BI-WEEKLY)|4020820171370029335

and suppose that I already have 100,000 records stored in my internal database. I do not need to
compare this new record (in worst case) to all the other records to see if "SABOURIN, JAMES"
from zip code "02895" has previously donated or not. I simply need to know if the tree structure
presently has a path: **SABOURIN, JAMES** --> **02895** or not, and if there is such a path, then
just I check to see if he has contributed in any years prioir to 2017.

![Donors tree structure](https://github.com/dchandan/donation-analytics/blob/master/Resources/Donors.png)

Note, we are not useing the committee to which a donation has been made because the problem
statement says that a donor is a repeat donor if he/she has "previously contributed
to any recipient listed in the `itcont.txt` file in any prior calendar year".


### The `RepeatDonations` class

The task of this class is to maintain a data structure of repeat donations. To be efficient, this
class also stores data in a **tree structure**.

### The `AnalyticsApp` class

This is "the application". It is adapted to streaming use. For any given string-record, e.g.

```python
record_string = "C00629618|N|TER|P|201701230300133512|15C|IND|PEREZ, JOHN A|LOS ANGELES|CA|90017|PRINCIPAL|DOUBLE NICKEL ADVISORS|01032017|40|H6CA34245|SA01251735122|1141239|||2012520171368850783"
```

regardless of whether it is read from file or from a streaming API, one simply has to do

```python
app.update(record_string)
```

This function
1. Creates a record object from the string
2. Checks if the donor in the record is a repeat donor
3. Prints the analysis to the output file
4. Finally enters the new record into its internal database

## Dependencies

This program only depends on two libraries not in the Python standard library: `numpy` and `pytest`
(for testing only).


## Instructions

The usage of the app is very simple:

1. Instantiate the `app` as `AnalyticsApp(output_filename, percentile_value)`.
2. For any new string-record, simply update the app as `app.update(record_string)`. This one step does everything as described above.
3. At the end of the app call `app.finalize()`.


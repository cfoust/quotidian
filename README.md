Quotidian: A simple platform for unifying the data in your life.

At face value, the project seems relatively simple and not all that innovative,
but it shines just because it unifies everything into one single place. As an
avid hobbyist of collecting lots of (admittedly insignificant) data about my
life, I realized that when I would write programs to work with it and come up
with interesting trends, I was often implementing code that followed a similar
pattern and would be better served if it was abstracted away a little bit.

So that's what this project aims to do. The general idea is that each source
of data is abstracted into a module found in the quotidian/modules directory. 
Each module knows how to take some files in a directory and turn it into 
timestamped JSON-serializable objects. The role of quotidian is to be the
caretaker of this data and to store it, so that it doesn't have to be generated
and reparsed every time. It's deceptively simple, but can be very powerful
when trying to correlate different kinds of data over time, especially with
the moduling system.

The library has a Collection object that takes in a folder as an argument 
during instantiation. Within that folder, the library generates a small readme
with the various data sources that it can understand and some short instructions
on how to get it and make it accessible to the program. Each module is restricted
to accessing data in its own folder (though this is not enforced by any sort of
watchdog, it's just a loose rule) and SHOULD NOT change any of the data. 

After the data is parsed, it's stored into an SQLite database that sits in the
collection's main directory. There is no special schema here, it just stores
the parsed data with a timestamp and a json for each one, which can save some
computational time, especially when HTML has to be parsed to get the data 
initially.
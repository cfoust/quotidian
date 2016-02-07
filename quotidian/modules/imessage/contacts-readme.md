So I ran into a bunch of problems with trying to parse the AddressBook.sqlitedb file. It doesn't play nice with the version of sqlite that ships with python, so you end up having to open it with the sqlite command line tools. I ran the following to get a workable contact list after opening up the db in the sqlite3 cli.
	
	.mode csv
	.output people.csv

	select ABPerson.ROWID
     , ABPerson.first
     , ABPerson.last
     , ABPerson.Organization as organization
     , ABPerson.Department as department
     , ABPerson.Birthday as birthday
     , ABPerson.JobTitle as jobtitle

     , (select value from ABMultiValue where property = 3 and record_id = ABPerson.ROWID and label = (select ROWID from ABMultiValueLabel where value = '_$!<Work>!$_')) as phone_work
     , (select value from ABMultiValue where property = 3 and record_id = ABPerson.ROWID and label = (select ROWID from ABMultiValueLabel where value = '_$!<Mobile>!$_')) as phone_mobile
     , (select value from ABMultiValue where property = 3 and record_id = ABPerson.ROWID and label = (select ROWID from ABMultiValueLabel where value = '_$!<Home>!$_')) as phone_home

     , (select value from ABMultiValue where property = 4 and record_id = ABPerson.ROWID and label is null) as email
     
     , (select value from ABMultiValueEntry where parent_id in (select ROWID from ABMultiValue where record_id = ABPerson.ROWID) and key = (select ROWID from ABMultiValueEntryKey where lower(value) = 'street')) as address
     , (select value from ABMultiValueEntry where parent_id in (select ROWID from ABMultiValue where record_id = ABPerson.ROWID) and key = (select ROWID from ABMultiValueEntryKey where lower(value) = 'city')) as city
	 from ABPerson
	 order by ABPerson.ROWID
	;

(The select there is taken from https://gist.github.com/laacz/1180765)
This generates a file, people.csv, that we use in the parser if it exists.

In order to really get this working, I'd have to likely install Python 3.1 and see if peewee can play nice with the AddressBook database. Until then, this is a workaround that is pretty quick.
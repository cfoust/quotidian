#!/usr/bin/env python

import datetime
import dateutil.parser
import re

"""Takes in an array of (often command-line) arguments that are probably
dates and validity checks them. Has a sort-of intelligent way of choosing the
range. Allows for expressions like, -3w or +3w and all that. Returns a tuple in
the format of (start [datetime], end [datetime], rest of arguments [array]).

Removes the very first argument because that's usually the script file name."""
deltaPattern = re.compile('^([+-])([\d])([hdwmy])$')
yearPattern = re.compile('^year([\d])$')
def argsToRange(args):
	start = None
	end = None
	for arg in args:
		if arg == 'all': # For all data
			if len(args) > 1:
				rest = args[1:]
			else:
				rest = []
			return (datetime.datetime.min,
				    datetime.datetime.max,
				    rest)
		try:
			parsed = dateutil.parser.parse(arg)
		except:
			if deltaPattern.match(arg):
				match = deltaPattern.match(arg)
				sign = match.group(1)
				num = int(match.group(2))
				type = match.group(3)

				if sign == '-':
					num *= -1

				if type == 'h':
					delta = datetime.timedelta(hours = num)
				elif type == 'd':
					delta = datetime.timedelta(hours = 24*num)
				elif type == 'w':
					delta = datetime.timedelta(weeks = num)
				elif type == 'm':
					delta = datetime.timedelta(weeks = num*4)
				elif type == 'y':
					delta = datetime.timedelta(weeks = num*52)

				if not start:
					start = datetime.datetime.now() + delta
					continue
				elif not end:
					end = start + delta
					break
			elif yearPattern.match(arg):
				# This is just for me for various reasons. Not really useful
				# to anyone else, but considering I'm the only contributor/user..
				# it's no big deal.
				match = yearPattern.match(arg)
				num = int(match.group(1)) - 1

				if num == 0:
					start = datetime.datetime(2010,12,4)
				else:
					start = datetime.datetime(2011+num,1,28)
				end = datetime.datetime(2011 + num + 1,1,27)

				if len(args) > 1:
					rest = args[1:]
				else:
					rest = []
				return (start,
					    end,
					    rest)
			elif arg == 'now':
				now = datetime.datetime.now()
				if not start:
					start = now
				elif not end:
					end = now
				continue
			elif arg == 'today':
				s = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
				if not start:
					start = s
				elif not end:
					end = s
				continue
			else:
				raise Exception('There was an error in getting a date from "%s".' % arg)

		if not start:
			start = parsed
			continue
		elif not end:
			end = parsed
			break


	if start > end:
		temp = end
		end = start
		start = temp

	if len(args) > 2:
		rest = args[2:]
	else:
		rest = []
	return (start,
		    end,
		    rest)
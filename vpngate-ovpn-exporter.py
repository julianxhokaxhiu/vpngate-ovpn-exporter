'''
The MIT License (MIT)

Copyright (c) 2016 Julian Xhokaxhiu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import sys, os, csv, codecs, base64, getopt

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

# Get Country as argument
countryArgument = '*'
opts, args = getopt.getopt(sys.argv[1:], 'c:')
for o, a in opts:
    if o == '-c' and len(a) > 0:
        countryArgument = a

# Download the CSV file and prepare for parsing
url = "http://www.vpngate.net/api/iphone/"
ftpstream = urlopen(url)
csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))

# Prepare variable placeholders for needed column indexes
hostNameIndex = -1
countryShortIndex = -1
openVPNConfigDataIndex = -1

# Line reading counter ( when i > 2, it means we're beginnig to read the VPN configurations )
i = 0

# Start reading the CSV file
for line in csvfile:
    # Get Short Contry index column ( ex. IT, FR, DE, etc. )
    try:
        countryShortIndex = line.index('CountryShort')
    except Exception as e:
        pass # Fail silently

    # Get OpenVPN configuration index column ( encoded in Base64 )
    try:
        openVPNConfigDataIndex = line.index('OpenVPN_ConfigData_Base64')
    except Exception as e:
        pass # Fail silently

    # Get Hostname index column ( useful to save the configuration as filename later )
    try:
        hostNameIndex = line.index('#HostName')
    except Exception as e:
        pass # Fail silently

    # If we have found valid column indexes ( which means we read the line 2 ) and we're in the configuration section ( i > 2)
    if countryShortIndex > -1 and openVPNConfigDataIndex > -1 and hostNameIndex > -1 and i > 2:
        try:
            # If country code matches the one given as argument, or no one was given ( which means just get all )
            if line[countryShortIndex] == countryArgument or countryArgument == '*':
                # Create folders based on country code...
                os.makedirs( line[countryShortIndex], exist_ok=True )
                # ...and save their respective OpenVPN configuration in a file ( binary mode needed )
                f = open( line[countryShortIndex] + '/' + line[hostNameIndex] + '.ovpn', 'wb')
                f.write( base64.b64decode(line[openVPNConfigDataIndex]) )
                f.close()
        except:
            # If any error occours just ignore it
            pass

    # Count the line as readed
    i+=1
# vpngate-ovpn-exporter
Export all VPNGate OpenVPN configurations to files inside country-code relative folders

## Options
```
 - c <COUNTRY_CODE>
   ISO 3166-1 Country code list ( for ex. IT, DE, FR, etc. ). See https://en.wikipedia.org/wiki/ISO_3166-1
```

## Usage
If you want to export only IT country code:
```
python vpngate-ovpn-exporter.py -c IT
```
otherwise if you want to export all the configurations:
```
python vpngate-ovpn-exporter.py
```

## Example of the export
```
  ./
  -> JP/
    -> vpn749959923.ovpn
  -> SG/
    -> vpn847862700.ovpn
```

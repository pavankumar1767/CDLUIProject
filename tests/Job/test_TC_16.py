#
#
# import pytest
# import httpx
# from base64 import b64encode
# import xml.etree.ElementTree as ET
# import xml.sax.saxutils as saxutils
# import csv
#
#
# class TestSoapRequest:
#
#     @classmethod
#     def setup_class(cls):
#         cls.url = "https://rockpegion-qa.sigmastream.com/WITSMLStore/services/Store"
#         cls.username = "dasharathichakaravarthy"
#         cls.password = "gIdH8nZ"
#         cls.auth_header = b64encode(f"{cls.username}:{cls.password}".encode()).decode()
#
#         cls.headers = {
#             "Content-Type": "text/xml; charset=utf-8",
#             "SOAPAction": "http://www.witsml.org/message/120/WMLS_GetFromStore",
#             "Authorization": f"Basic {cls.auth_header}"
#         }
#
#         cls.soap_body = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
#                          xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/"
#                          xmlns:tns="http://www.witsml.org/wsdl/120"
#                          xmlns:types="http://www.witsml.org/wsdl/120/encodedTypes"
#                          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
#                          xmlns:xsd="http://www.w3.org/2001/XMLSchema">
#           <soap:Body soap:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
#             <q1:WMLS_GetFromStore xmlns:q1="http://www.witsml.org/message/120">
#               <WMLtypeIn xsi:type="xsd:string">mudLog</WMLtypeIn>
#               <QueryIn xsi:type="xsd:string">&lt;mudLogs xmlns="http://www.witsml.org/schemas/1series" version="1.4.1.1"&gt;
#           &lt;mudLog uidWell="6F35D63E-4AE8-45F5-A067-E4205073DD91_1172" uidWellbore="F1B2BCAE-FDCF-4FD9-AB58-CD8B4AC02643_1172" uid="4TJMG30"&gt;
#             &lt;nameWell /&gt;
#             &lt;nameWellbore /&gt;
#             &lt;name /&gt;
#           &lt;/mudLog&gt;
#         &lt;/mudLogs&gt;</QueryIn>
#               <OptionsIn xsi:type="xsd:string">returnElements=all</OptionsIn>
#             </q1:WMLS_GetFromStore>
#           </soap:Body>
#         </soap:Envelope>"""
#
#         cls.response_text = None
#
#     def test_send_soap_request(self):
#         # Send SOAP request
#         response = httpx.post(self.url, content=self.soap_body, headers=self.headers, verify=False)
#         assert response.status_code == 200
#
#         self.__class__.response_text = response.text
#
#         # Parse SOAP response
#         root = ET.fromstring(self.response_text)
#
#         ns_soapenv = "http://schemas.xmlsoap.org/soap/envelope/"
#         ns_ns1 = "http://www.witsml.org/message/120"
#         ns = {
#             "soapenv": ns_soapenv,
#             "ns1": ns_ns1
#         }
#         body = root.find("soapenv:Body", ns)
#         response = body.find("ns1:WMLS_GetFromStoreResponse", ns)
#         xmlout = response.find("XMLout", ns).text
#
#         # Unescape the inner XML string
#         inner_xml_str = saxutils.unescape(xmlout)
#
#         # Parse inner XML
#         mudlogs_root = ET.fromstring(inner_xml_str)
#
#         # Namespace for mudLogs
#         ns_witsml = {"w": "http://www.witsml.org/schemas/1series"}
#
#         geology_intervals = mudlogs_root.findall(".//w:geologyInterval", ns_witsml)
#
#         print(f"\nTotal geologyInterval elements found: {len(geology_intervals)}\n")
#
#         total_lithology_count = 0
#
#         # Prepare list of rows for CSV
#         rows = []
#
#         for gi in geology_intervals:
#             gi_uid = gi.attrib.get("uid", "No UID")
#             lithologies = gi.findall(".//w:lithology", ns_witsml)
#             lith_count = len(lithologies)
#             total_lithology_count += lith_count
#
#             lith_uids = [l.attrib.get("uid", "No UID") for l in lithologies]
#
#             print(f"geologyInterval UID: {gi_uid} - Lithology count: {lith_count}")
#             for lith_uid in lith_uids:
#                 print(f"  Lithology UID: {lith_uid}")
#             print()
#
#             # Add a row per lithology, or if no lithologies add one row with empty lithology data
#             if lith_count > 0:
#                 for lith_uid in lith_uids:
#                     rows.append([gi_uid, lith_count, lith_uid])
#             else:
#                 rows.append([gi_uid, 0, "No Lithology"])
#
#         print("==== Summary ====")
#         print(f"Total geologyInterval count: {len(geology_intervals)}")
#         print(f"Total lithology count: {total_lithology_count}")
#
#         # Write CSV file
#         with open("geology_lithology_report.csv", mode="w", newline="", encoding="utf-8") as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerow(["GeologyInterval UID", "Lithology Count", "Lithology UID"])
#             writer.writerows(rows)
#
#         print("\nCSV report 'geology_lithology_report.csv' generated successfully.")





















import pytest
import httpx
from base64 import b64encode
import xml.etree.ElementTree as ET
import xml.sax.saxutils as saxutils
import csv


class TestSoapRequest:

    @classmethod
    def setup_class(cls):
        cls.url = "https://rockpegion-qa.sigmastream.com/WITSMLStore/services/Store"
        cls.username = "dasharathichakaravarthy"
        cls.password = "gIdH8nZ"
        cls.auth_header = b64encode(f"{cls.username}:{cls.password}".encode()).decode()

        cls.headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": "http://www.witsml.org/message/120/WMLS_GetFromStore",
            "Authorization": f"Basic {cls.auth_header}"
        }

        cls.soap_body = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
                         xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/" 
                         xmlns:tns="http://www.witsml.org/wsdl/120" 
                         xmlns:types="http://www.witsml.org/wsdl/120/encodedTypes" 
                         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                         xmlns:xsd="http://www.w3.org/2001/XMLSchema">
          <soap:Body soap:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <q1:WMLS_GetFromStore xmlns:q1="http://www.witsml.org/message/120">
              <WMLtypeIn xsi:type="xsd:string">mudLog</WMLtypeIn>
              <QueryIn xsi:type="xsd:string">&lt;mudLogs xmlns="http://www.witsml.org/schemas/1series" version="1.4.1.1"&gt;
          &lt;mudLog uidWell="6F35D63E-4AE8-45F5-A067-E4205073DD91_1081" uidWellbore="F1B2BCAE-FDCF-4FD9-AB58-CD8B4AC02643_1081" uid="4TJMG30"&gt;
            &lt;nameWell /&gt;
            &lt;nameWellbore /&gt;
            &lt;name /&gt;
          &lt;/mudLog&gt;
        &lt;/mudLogs&gt;</QueryIn>
              <OptionsIn xsi:type="xsd:string">returnElements=all</OptionsIn>
            </q1:WMLS_GetFromStore>
          </soap:Body>
        </soap:Envelope>"""

        cls.response_text = None

    def test_send_soap_request(self):
        # Send SOAP request
        response = httpx.post(self.url, content=self.soap_body, headers=self.headers, verify=False)
        assert response.status_code == 200

        self.__class__.response_text = response.text

        # Parse SOAP response
        root = ET.fromstring(self.response_text)

        ns_soapenv = "http://schemas.xmlsoap.org/soap/envelope/"
        ns_ns1 = "http://www.witsml.org/message/120"
        ns = {
            "soapenv": ns_soapenv,
            "ns1": ns_ns1
        }
        body = root.find("soapenv:Body", ns)
        response = body.find("ns1:WMLS_GetFromStoreResponse", ns)
        xmlout = response.find("XMLout", ns).text

        # Unescape the inner XML string
        inner_xml_str = saxutils.unescape(xmlout)

        # Parse inner XML
        mudlogs_root = ET.fromstring(inner_xml_str)

        # Namespace for mudLogs
        ns_witsml = {"w": "http://www.witsml.org/schemas/1series"}

        geology_intervals = mudlogs_root.findall(".//w:geologyInterval", ns_witsml)

        print(f"\nTotal geologyInterval elements found: {len(geology_intervals)}\n")

        total_lithology_count = 0
        rows = []

        for gi in geology_intervals:
            gi_uid = gi.attrib.get("uid", "No UID")
            lithologies = gi.findall(".//w:lithology", ns_witsml)
            lith_count = len(lithologies)
            total_lithology_count += lith_count

            lith_uids = [l.attrib.get("uid", "No UID") for l in lithologies]

            print(f"geologyInterval UID: {gi_uid} - Lithology count: {lith_count}")
            for lith_uid in lith_uids:
                print(f"  Lithology UID: {lith_uid}")
            print()

            if lith_count > 0:
                for lith_uid in lith_uids:
                    rows.append([gi_uid, lith_count, lith_uid])
            else:
                rows.append([gi_uid, 0, "No Lithology"])

        print("==== Summary ====")
        print(f"Total geologyInterval count: {len(geology_intervals)}")
        print(f"Total lithology count: {total_lithology_count}")

        # Write to CSV
        with open("geology_lithology_report.csv", mode="w", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["GeologyInterval UID", "Lithology Count", "Lithology UID"])
            writer.writerows(rows)

            # Add totals at the end
            writer.writerow([])
            writer.writerow(["Total GeologyIntervals", len(geology_intervals), ""])
            writer.writerow(["Total Lithologies", total_lithology_count, ""])

        print("\nCSV report 'geology_lithology_report.csv' generated successfully.")

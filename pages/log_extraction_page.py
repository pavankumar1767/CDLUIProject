import csv
import os
import logging
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from requests.auth import HTTPBasicAuth
import requests

class LogExtractionPage:
    def __init__(self, config, test_data):
        self.endpoint = config.WITSML_URL
        self.username = config.user
        self.password = config.rp_password
        self.csv_file = "log_data.csv"
        self.index_type = test_data["TimeLog"]["INDEX_TYPE"]
        self.start_index = test_data["TimeLog"]["StartTime1"]
        self.end_index = test_data["TimeLog"]["EndTime1"]
        self.uid_well = "3001548007_1207"
        self.uid_wellbore = "3001548007-ST00BP00_1207"
        self.uid_log = "TIME_PITS"

        logging.basicConfig(
            filename='log_extraction.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def build_soap_body(self, start_index, end_index):
        return f"""<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                       xmlns:xsd="http://www.w3.org/2001/XMLSchema">
          <soap:Body>
            <q1:WMLS_GetFromStore xmlns:q1="http://www.witsml.org/message/120">
              <WMLtypeIn xsi:type="xsd:string">log</WMLtypeIn>
              <QueryIn xsi:type="xsd:string">
                &lt;logs xmlns="http://www.witsml.org/schemas/1series" version="1.4.1.1"&gt;
                  &lt;log uidWell="{self.uid_well}" uidWellbore="{self.uid_wellbore}" uid="{self.uid_log}"&gt;
                    &lt;startDateTimeIndex&gt;{start_index}&lt;/startDateTimeIndex&gt;
                    &lt;endDateTimeIndex&gt;{end_index}&lt;/endDateTimeIndex&gt;
                  &lt;/log&gt;
                &lt;/logs&gt;
              </QueryIn>
              <OptionsIn xsi:type="xsd:string">returnElements=data-only</OptionsIn>
            </q1:WMLS_GetFromStore>
          </soap:Body>
        </soap:Envelope>
        """

    def fetch_log_data(self, soap_body):
        response = requests.post(
            self.endpoint,
            data=soap_body.encode("utf-8"),
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": "http://www.witsml.org/message/120/WMLS_GetFromStore"
            },
            auth=HTTPBasicAuth(self.username, self.password)
        )
        return response.content if response.status_code == 200 else None

    def parse_and_append_to_csv(self, xml_response):
        ns = {
            "soap": "http://schemas.xmlsoap.org/soap/envelope/",
            "wmls": "http://www.witsml.org/message/120",
            "witsml": "http://www.witsml.org/schemas/1series"
        }

        root = ET.fromstring(xml_response)
        xml_out_elem = root.find(".//wmls:WMLS_GetFromStoreResponse/XMLout", ns)
        if xml_out_elem is None or not xml_out_elem.text:
            return [], None

        log_root = ET.fromstring(xml_out_elem.text)
        log = log_root.find("witsml:log", ns)
        if log is None:
            return [], None

        data_nodes = log.findall("witsml:logData/witsml:data", ns)
        if not data_nodes:
            return [], None

        rows = [node.text.split(",") for node in data_nodes]
        last_time = None
        try:
            last_time = datetime.strptime(rows[-1][0], "%Y-%m-%dT%H:%M:%S.%fZ")
        except:
            try:
                last_time = datetime.strptime(rows[-1][0], "%Y-%m-%dT%H:%M:%SZ")
            except:
                pass

        if not os.path.exists(self.csv_file):
            mnemonic_list = log.find("witsml:logData/witsml:mnemonicList", ns)
            if mnemonic_list is not None:
                with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(mnemonic_list.text.split(","))

        with open(self.csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        return rows, last_time

    def extract_log_data(self):
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

        start_dt = datetime.strptime(self.start_index, "%Y-%m-%dT%H:%M:%S.%fZ")
        end_dt = datetime.strptime(self.end_index, "%Y-%m-%dT%H:%M:%S.%fZ")
        iteration_count = 0

        while start_dt < end_dt:
            iteration_count += 1
            logging.info(f"Iteration {iteration_count}: Fetching data from {start_dt} to {end_dt}")

            soap_body = self.build_soap_body(
                start_dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-3] + "Z",
                end_dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-3] + "Z"
            )

            xml_response = self.fetch_log_data(soap_body)
            if not xml_response:
                logging.warning("No response or error.")
                break

            rows, last_time = self.parse_and_append_to_csv(xml_response)
            if not rows or not last_time or last_time <= start_dt:
                logging.warning("No new data or failed to advance start time.")
                break

            start_dt = last_time + timedelta(milliseconds=1)

        logging.info(f"Log extraction complete. Total iterations: {iteration_count}")

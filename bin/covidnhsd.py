import sys, logging
import csv
import requests
import json
from lxml import html
from StringIO import StringIO
from helpers import load_checkpoint, save_checkpoint, print_xml_stream, get_input_config, get_validation_config, do_validate


#set up logging
logging.root
logging.root.setLevel(logging.WARNING)
formatter = logging.Formatter('%(levelname)s %(message)s')
#with zero args , should go to STD ERR
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.root.addHandler(handler)


SCHEME = """<scheme>
    <title>Covid-19 NHS Digital</title>
    <description>Poll for NHS Digital COVID-19 data</description>
    <use_external_validation>true</use_external_validation>
    <streaming_mode>xml</streaming_mode>
    <use_single_instance>false</use_single_instance>

    <endpoint>
        <args>
            <arg name="name">
                <title>Covid input name</title>
                <description>Name of this input</description>
            </arg>
            <arg name="http_proxy">
                <title>HTTP Proxy Address</title>
                <description>HTTP Proxy Address</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="https_proxy">
                <title>HTTPs Proxy Address</title>
                <description>HTTPs Proxy Address</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="section">
                <title>Data Section</title>
                <description>Dataset to poll? (nhs111 or pathways)</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
        </args>
    </endpoint>
</scheme>
"""

def do_run():

    config = get_input_config()

    #setup some globals
    global STANZA
    STANZA = config.get("name")

    SECTION = config.get("section")


    #params
    request_timeout = int(config.get("request_timeout", 30))
    http_proxy = config.get("http_proxy")
    https_proxy = config.get("https_proxy")
    proxies = {}

    if not http_proxy is None:
        proxies["http"] = http_proxy
    if not https_proxy is None:
        proxies["https"] = https_proxy

    req_args = {"verify" : True , "timeout" : float(request_timeout)}

    if proxies:
        req_args["proxies"] = proxies


    page = requests.get('https://digital.nhs.uk/data-and-information/publications/statistical/mi-potential-covid-19-symptoms-reported-through-nhs-pathways-and-111-online/latest', params=req_args)
    page_dom = html.fromstring(page.content)
    urls = {}
    urls['pathways'] = page_dom.xpath('//a[@title="NHS Pathways Potential COVID-19 Open Data"]')[0].attrib['href']
    urls['nhs111'] = page_dom.xpath('//a[@title="111 Online Potential COIVD-19 Open Data"]')[0].attrib['href']
    urls['meta'] = page_dom.xpath('//a[@title="NHS Pathways and 111 Online Potential COVID-19 Open Data Descriptions"]')[0].attrib['href']
    urls['description'] = page_dom.xpath('//a[@title="NHS Pathways and 111 Online Potential COVID-19 Meta Data"]')[0].attrib['href']

    try:
        resp = requests.get(url=urls[SECTION], params=req_args)

        if not load_checkpoint(config, urls[SECTION]):
            c = StringIO()
            c.write(resp.content)
            c.seek(0)
            reader = csv.DictReader(c)
            for record in reader:
                empty_keys = [k for k,v in record.iteritems() if not v]
                #Tidy some fields
                for k in empty_keys:
                    del record[k]
                print_xml_stream(json.dumps(record,ensure_ascii=False),SECTION)
            #handle_output(content,daily_report.name)
            logging.warning("Logging file={}".format(urls[SECTION]))
            save_checkpoint(config, urls[SECTION])

        logging.info("Finished")

    except RuntimeError, e:
        logging.error("Looks like an error: %s" % str(e))
        sys.exit(2)

def usage():
    print "usage: %s [--scheme|--validate-arguments]"
    logging.error("Incorrect Program Usage")
    sys.exit(2)

def do_scheme():
    print SCHEME

if __name__ == '__main__':

    if len(sys.argv) > 1:
        if sys.argv[1] == "--scheme":
            do_scheme()
        elif sys.argv[1] == "--validate-arguments":
            do_validate()
        else:
            usage()
    else:
        do_run()

    sys.exit(0)


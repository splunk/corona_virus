import md5
import sys
import xml.dom.minidom
import os
import time


# prints XML stream
def print_xml_stream(s,source,timestamp=False):
    if timestamp:
        timenow = time.time()
        print "<stream><event unbroken=\"1\"><time>%s</time><source>%s</source><data>%s</data><done/></event></stream>" % (timenow, source, encodeXMLText(s))
    else:
        print "<stream><event unbroken=\"1\"><source>%s</source><data>%s</data><done/></event></stream>" % (source, encodeXMLText(s))


def do_validate():
    config = get_validation_config()

def save_checkpoint(config, url):
    chk_file = get_encoded_file_path(config, url)
    # just create an empty file name
    f = open(chk_file, "w")
    f.close()

def load_checkpoint(config, url):
    chk_file = get_encoded_file_path(config, url)
    # try to open this file
    try:
        open(chk_file, "r").close()
    except:
        # assume that this means the checkpoint is not there
        return False
    return True

def get_encoded_file_path(config, url):
    # encode the URL (simply to make the file name recognizable)
    name = "covid"
    for i in range(len(url)):
        if url[i].isalnum():
            name += url[i]
        else:
            name += "_"

    # MD5 the URL
    m = md5.new()
    m.update(url)
    name += "_" + m.hexdigest()

    return os.path.join(config["checkpoint_dir"], name)


def dictParameterToStringFormat(parameter):

    if parameter:
        return ''.join('{}={},'.format(key, val) for key, val in parameter.items())[:-1]
    else:
        return None


def handle_output(output, source, timestamp=False):

    try:
        print_xml_stream(output, source, timestamp=timestamp)
        sys.stdout.flush()
    except RuntimeError, e:
        print("Looks like an error handle the response output: %s" % str(e))

# prints validation error data to be consumed by Splunk
def print_validation_error(s):
    print "<error><message>%s</message></error>" % encodeXMLText(s)

# prints XML stream
def print_xml_single_instance_mode(s):
    print "<stream><event><data>%s</data></event></stream>" % encodeXMLText(s)

# prints simple stream
def print_simple(s):
    print "%s\n" % s

def encodeXMLText(text):
    text = text.replace("&", "&amp;")
    text = text.replace("\"", "&quot;")
    text = text.replace("'", "&apos;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text

def usage():
    print "usage: %s [--scheme|--validate-arguments]"
    sys.exit(2)

#read XML configuration passed from splunkd, need to refactor to support single instance mode
def get_input_config():
    config = {}

    try:
        # read everything from stdin
        config_str = sys.stdin.read()

        # parse the config XML
        doc = xml.dom.minidom.parseString(config_str)
        root = doc.documentElement

        session_key_node = root.getElementsByTagName("session_key")[0]
        if session_key_node and session_key_node.firstChild and session_key_node.firstChild.nodeType == session_key_node.firstChild.TEXT_NODE:
            data = session_key_node.firstChild.data
            config["session_key"] = data

        server_uri_node = root.getElementsByTagName("server_uri")[0]
        if server_uri_node and server_uri_node.firstChild and server_uri_node.firstChild.nodeType == server_uri_node.firstChild.TEXT_NODE:
            data = server_uri_node.firstChild.data
            config["server_uri"] = data

        conf_node = root.getElementsByTagName("configuration")[0]
        if conf_node:
            stanza = conf_node.getElementsByTagName("stanza")[0]
            if stanza:
                stanza_name = stanza.getAttribute("name")
                if stanza_name:
                    config["name"] = stanza_name

                    params = stanza.getElementsByTagName("param")
                    for param in params:
                        param_name = param.getAttribute("name")
                        if param_name and param.firstChild and \
                           param.firstChild.nodeType == param.firstChild.TEXT_NODE:
                            data = param.firstChild.data
                            config[param_name] = data

        checkpoint_node = root.getElementsByTagName("checkpoint_dir")[0]
        if checkpoint_node and checkpoint_node.firstChild and \
                checkpoint_node.firstChild.nodeType == checkpoint_node.firstChild.TEXT_NODE:
            config["checkpoint_dir"] = checkpoint_node.firstChild.data

        if not config:
            raise Exception, "Invalid configuration received from Splunk."


    except Exception, e:
        raise Exception, "Error getting Splunk configuration via STDIN: %s" % str(e)

    return config

#read XML configuration passed from splunkd, need to refactor to support single instance mode
def get_validation_config():
    val_data = {}

    # read everything from stdin
    val_str = sys.stdin.read()

    # parse the validation XML
    doc = xml.dom.minidom.parseString(val_str)
    root = doc.documentElement

    item_node = root.getElementsByTagName("item")[0]
    if item_node:

        name = item_node.getAttribute("name")
        val_data["stanza"] = name

        params_node = item_node.getElementsByTagName("param")
        for param in params_node:
            name = param.getAttribute("name")
            if name and param.firstChild and \
               param.firstChild.nodeType == param.firstChild.TEXT_NODE:
                val_data[name] = param.firstChild.data

    return val_data

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


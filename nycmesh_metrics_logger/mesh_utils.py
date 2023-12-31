import re

def nn_from_string(input_string):
    matches = re.findall("(\d{3,})", input_string)
    if not matches:
        return None

    return int(re.findall("(\d{3,})", input_string)[0])

def identifier_string_from_string_multi(input_string, position=0):
    matches = re.findall("(\d{3,})", input_string)
    if len(matches)==0:
        return input_string
    if len(matches)==1 and position==0:
        return input_string
    if len(matches)==1 and position==1:
        return ''
    matches.sort()
    return matches[position]


def nn_to_ip(nn):
    ip_fourth_octet=nn%100
    ip_third_octet=int((nn-ip_fourth_octet)/100)
    ip = f"10.69.{ip_third_octet}.{ip_fourth_octet}"
    return ip

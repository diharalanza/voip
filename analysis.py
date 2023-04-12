#Author Braeden Brooking
#Source from https://www.proquest.com/docview/1980476483?pq-origsite=primo

import dpkt
import pyshark
import netifaces
import socket
import pygeoip
import os


def detectInterface():
    interfaceList = netifaces.interfaces()
    print("Select an interface for packet sniffing:")

    for i in range(len(interfaceList)):
        print(f"{i+1}. {interfaceList[i]}")

    choice = int(input())
    interfaceName = interfaceList[choice-1]

    print(f"Using interface: {interfaceName}")
    return interfaceName


def captureTraffic(interfaceName, duration=50):
    capture = pyshark.LiveCapture(interface=interfaceName)
    capture.sniff(timeout=duration)
    filename = f"{interfaceName}_output.pcap"
    capture.save(filename)

    print(f"Captured {len(capture)} packets and saved to {filename}")
    return filename


# Remove anomalies
def editcap(input_file):
    output_file = f"{os.path.splitext(input_file)[0]}_editcap.pcap"
    os.system(f"editcap -d {input_file} {output_file}")

    print(f"Edited {input_file} and saved as {output_file}")
    return output_file


def menu():
    print("Select an option from the menu:")
    print("1. Display geographic location of captured IP data")
    print("2. Print source port to destination port of captured IP data with destination port 5060")
    print("3. Extract and display RTP packets from captured data")
    print("4. Quit")

    choice = int(input(">> "))
    if choice > 4 or choice < 0:
        print("Invalid choice")
        return menu()
    else:
        return choice


# Option 1
def printGeoLocation(capFile):
    with open(capFile, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        geoIP = pygeoip.GeoIP('GeoLiteCity.dat')

        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data

            sourceIP = socket.inet_ntoa(ip.src)
            destinationIP = socket.inet_ntoa(ip.dst)

            print(f"{sourceIP} -> {destinationIP}: {geoIP.record_by_addr(destinationIP)}")


# Option 2
def printPorts(capFile):
    with open(capFile, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data

            if isinstance(ip.data, dpkt.udp.UDP):
                udp = ip.data

                if udp.dport == 5060:
                    print(f"{socket.inet_ntoa(ip.src)}:{udp.sport} -> {socket.inet_ntoa(ip.dst)}:{udp.dport}")


# Option 3
def extractRTPPackets(capFile):
    os.system(f"tshark -r {capFile} -Y rtp")


if __name__ == "__main__":
    interfaceName = detectInterface()
    capFile = captureTraffic(interfaceName)
    editcapFile = editcap(capFile)

    while True:
        choice = menu()
        if choice == 1:
            printGeoLocation(editcapFile)
        elif choice == 2:
            printPorts(editcapFile)
        elif choice == 3:
            extractRTPPackets(editcapFile)
        else:
            break
    

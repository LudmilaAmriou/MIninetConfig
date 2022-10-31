#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    r2 = net.addHost('r2', cls=Node, ip='10.15.64.2/19')
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')
    r1 = net.addHost('r1', cls=Node, ip='10.15.64.1/19')
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.15.0.2/19', defaultRoute='via 10.15.0.1/19')
    h3 = net.addHost('h3', cls=Host, ip='10.15.96.2/19', defaultRoute='via 10.15.96.1/19')
    h2 = net.addHost('h2', cls=Host, ip='10.15.32.2/19', defaultRoute='via 10.15.32.1/19')
    h4 = net.addHost('h4', cls=Host, ip='10.15.128.2/19', defaultRoute='via 10.15.128.1/19')

    info( '*** Add links\n')
    net.addLink(r1, r2)
    net.addLink(r2, h3)
    net.addLink(r2, h4)
    net.addLink(r1, h1)
    net.addLink(r1, h2)

    info( '*** Starting network\n')
    net.build()
    r1.cmd("ifconfig r1-eth0 add 10.15.64.1/19")
    r1.cmd("ifconfig r1-eth0 up")
    r1.cmd("ip addr add 10.15.0.1/19 brd + dev r1-eth1")
    r1.cmd("ifconfig r1-eth1 up")
    r1.cmd("ip addr add 10.15.32.1/19 brd + dev r1-eth2")
    r1.cmd("ifconfig r1-eth2 up")
    r2.cmd("ip addr add 10.15.64.2/19 brd + dev r2-eth0")
    r2.cmd("ifconfig r2-eth0 up")
    r2.cmd("ip addr add 10.15.96.1/19 brd + dev r2-eth1")
    r2.cmd("ifconfig r2-eth1 up")
    r2.cmd("ip addr add 10.15.128.1/19 brd + dev r2-eth2")
    r2.cmd("ifconfig r2-eth2 up")
    h1.cmd("ip route add default via 10.15.0.1")
    h2.cmd("ip route add default via 10.15.32.1")
    h3.cmd("ip route add default via 10.15.96.1")
    h4.cmd("ip route add default via 10.15.128.1")
    r1.cmd("ip route add 10.15.96.0/19 via 10.15.64.2 dev r1-eth0")
    r1.cmd("ip route add 10.15.128.0/19 via 10.15.64.2 dev r1-eth0")
    r2.cmd("ip route add 10.15.0.0/19 via 10.15.64.1 dev r2-eth0")
    r2.cmd("ip route add 10.15.32.0/19 via 10.15.64.1 dev r2-eth0")
    info( '*** Starting controllers\n')

    for controller in net.controllers:
        controller.start()
    info( '*** Starting switches\n')

    info( '*** Post configure switches and hosts\n')

    CLI(net)

    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

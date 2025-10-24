from collections import defaultdict
from skidl import Pin, Part, Alias, SchLib, SKIDL, TEMPLATE

from skidl.pin import pin_types

SKIDL_lib_version = '0.0.1'

k1_motherboard_revA = SchLib(tool=SKIDL).add_parts(*[
        Part(**{ 'name':'R', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'R'}), 'ref_prefix':'R', 'fplist':[''], 'footprint':'Resistor_SMD:R_0603_1608Metric', 'keywords':'R res resistor', 'description':'Resistor', 'datasheet':'~', 'pins':[
            Pin(num='1',name='~',func=pin_types.PASSIVE,unit=1),
            Pin(num='2',name='~',func=pin_types.PASSIVE,unit=1)], 'unit_defs':[] }),
        Part(**{ 'name':'USB_C_Receptacle_USB2.0_14P', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'USB_C_Receptacle_USB2.0_14P'}), 'ref_prefix':'J', 'fplist':[''], 'footprint':'Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12', 'keywords':'usb universal serial bus type-C USB2.0', 'description':'USB 2.0-only 14P Type-C Receptacle connector', 'datasheet':'https://www.usb.org/sites/default/files/documents/usb_type-c.zip', 'pins':[
            Pin(num='S1',name='SHIELD',func=pin_types.PASSIVE,unit=1),
            Pin(num='A1',name='GND',func=pin_types.PASSIVE,unit=1),
            Pin(num='A12',name='GND',func=pin_types.PASSIVE,unit=1),
            Pin(num='B1',name='GND',func=pin_types.PASSIVE,unit=1),
            Pin(num='B12',name='GND',func=pin_types.PASSIVE,unit=1),
            Pin(num='A4',name='VBUS',func=pin_types.PASSIVE,unit=1),
            Pin(num='A9',name='VBUS',func=pin_types.PASSIVE,unit=1),
            Pin(num='B4',name='VBUS',func=pin_types.PASSIVE,unit=1),
            Pin(num='B9',name='VBUS',func=pin_types.PASSIVE,unit=1),
            Pin(num='A5',name='CC1',func=pin_types.BIDIR,unit=1),
            Pin(num='B5',name='CC2',func=pin_types.BIDIR,unit=1),
            Pin(num='A7',name='D-',func=pin_types.BIDIR,unit=1),
            Pin(num='B7',name='D-',func=pin_types.BIDIR,unit=1),
            Pin(num='A6',name='D+',func=pin_types.BIDIR,unit=1),
            Pin(num='B6',name='D+',func=pin_types.BIDIR,unit=1)], 'unit_defs':[] }),
        Part(**{ 'name':'Fuse', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'Fuse'}), 'ref_prefix':'F', 'fplist':[''], 'footprint':'Fuse:Fuse_1206_3216Metric', 'keywords':'fuse', 'description':'Fuse', 'datasheet':'~', 'pins':[
            Pin(num='1',name='~',func=pin_types.PASSIVE,unit=1),
            Pin(num='2',name='~',func=pin_types.PASSIVE,unit=1)], 'unit_defs':[] }),
        Part(**{ 'name':'D_TVS', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'D_TVS'}), 'ref_prefix':'D', 'fplist':[''], 'footprint':'Diode_SMD:D_SOD-323', 'keywords':'diode TVS thyrector', 'description':'Bidirectional transient-voltage-suppression diode', 'datasheet':'~', 'pins':[
            Pin(num='1',name='A1',func=pin_types.PASSIVE,unit=1),
            Pin(num='2',name='A2',func=pin_types.PASSIVE,unit=1)], 'unit_defs':[] }),
        Part(**{ 'name':'C', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'C'}), 'ref_prefix':'C', 'fplist':[''], 'footprint':'Capacitor_SMD:C_1206_3216Metric', 'keywords':'cap capacitor', 'description':'Unpolarized capacitor', 'datasheet':'~', 'pins':[
            Pin(num='1',name='~',func=pin_types.PASSIVE,unit=1),
            Pin(num='2',name='~',func=pin_types.PASSIVE,unit=1)], 'unit_defs':[] }),
        Part(**{ 'name':'Conn_01x02_Pin', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'Conn_01x02_Pin'}), 'ref_prefix':'J', 'fplist':[''], 'footprint':'Connector_Molex:Molex_MicroFit_3.0_1x02', 'keywords':'connector', 'description':'Generic connector, single row, 01x02, script generated', 'datasheet':'~', 'pins':[
            Pin(num='1',name='Pin_1',func=pin_types.PASSIVE,unit=1),
            Pin(num='2',name='Pin_2',func=pin_types.PASSIVE,unit=1)], 'unit_defs':[] }),
        Part(**{ 'name':'D', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'D'}), 'ref_prefix':'D', 'fplist':[''], 'footprint':'Diode_SMD:D_SOD-323', 'keywords':'diode', 'description':'Diode', 'datasheet':'~', 'pins':[
            Pin(num='1',name='K',func=pin_types.PASSIVE,unit=1),
            Pin(num='2',name='A',func=pin_types.PASSIVE,unit=1)], 'unit_defs':[] }),
        Part(**{ 'name':'Conn_01x03_Pin', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'Conn_01x03_Pin'}), 'ref_prefix':'J', 'fplist':[''], 'footprint':'Connector_Molex:Molex_KK-254_AE-6410-03A_1x03_P2.54mm_Vertical', 'keywords':'connector', 'description':'Generic connector, single row, 01x03, script generated', 'datasheet':'~', 'pins':[
            Pin(num='1',name='Pin_1',func=pin_types.PASSIVE,unit=1),
            Pin(num='2',name='Pin_2',func=pin_types.PASSIVE,unit=1),
            Pin(num='3',name='Pin_3',func=pin_types.PASSIVE,unit=1)], 'unit_defs':[] }),
        Part(**{ 'name':'Conn_01x04_Pin', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'Conn_01x04_Pin'}), 'ref_prefix':'J', 'fplist':[''], 'footprint':'Connector_JST:JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal', 'keywords':'connector', 'description':'Generic connector, single row, 01x04, script generated', 'datasheet':'~', 'pins':[
            Pin(num='1',name='Pin_1',func=pin_types.PASSIVE,unit=1),
            Pin(num='2',name='Pin_2',func=pin_types.PASSIVE,unit=1),
            Pin(num='3',name='Pin_3',func=pin_types.PASSIVE,unit=1),
            Pin(num='4',name='Pin_4',func=pin_types.PASSIVE,unit=1)], 'unit_defs':[] }),
        Part(**{ 'name':'24LC256', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'24LC256'}), 'ref_prefix':'U', 'fplist':['', ''], 'footprint':'Package_SO:SOIC-8_3.9x4.9mm_P1.27mm', 'keywords':'I2C Serial EEPROM', 'description':'I2C Serial EEPROM, 256Kb, DIP-8/SOIC-8/TSSOP-8/DFN-8', 'datasheet':'http://ww1.microchip.com/downloads/en/devicedoc/21203m.pdf', 'pins':[
            Pin(num='1',name='A0',func=pin_types.INPUT,unit=1),
            Pin(num='2',name='A1',func=pin_types.INPUT,unit=1),
            Pin(num='3',name='A2',func=pin_types.INPUT,unit=1),
            Pin(num='8',name='VCC',func=pin_types.PWRIN,unit=1),
            Pin(num='4',name='GND',func=pin_types.PWRIN,unit=1),
            Pin(num='5',name='SDA',func=pin_types.BIDIR,unit=1),
            Pin(num='6',name='SCL',func=pin_types.INPUT,unit=1),
            Pin(num='7',name='WP',func=pin_types.INPUT,unit=1)], 'unit_defs':[] }),
        Part(**{ 'name':'Conn_01x06_Pin', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'Conn_01x06_Pin'}), 'ref_prefix':'J', 'fplist':[''], 'footprint':'Connector_JST:JST_GH_BM06B-GHS-TBT_1x06-1MP_P1.25mm_Horizontal', 'keywords':'connector', 'description':'Generic connector, single row, 01x06, script generated', 'datasheet':'~', 'pins':[
            Pin(num='1',name='Pin_1',func=pin_types.PASSIVE,unit=1),
            Pin(num='2',name='Pin_2',func=pin_types.PASSIVE,unit=1),
            Pin(num='3',name='Pin_3',func=pin_types.PASSIVE,unit=1),
            Pin(num='4',name='Pin_4',func=pin_types.PASSIVE,unit=1),
            Pin(num='5',name='Pin_5',func=pin_types.PASSIVE,unit=1),
            Pin(num='6',name='Pin_6',func=pin_types.PASSIVE,unit=1)], 'unit_defs':[] }),
        Part(**{ 'name':'Conn_01x40_Pin', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'Conn_01x40_Pin'}), 'ref_prefix':'J', 'fplist':[''], 'footprint':'Connector_PinHeader_2.54mm:PinHeader_1x40_P2.54mm_Vertical', 'keywords':'connector', 'description':'Generic connector, single row, 01x40, script generated', 'datasheet':'~', 'pins':[
            Pin(num='1',name='Pin_1',func=pin_types.PASSIVE,unit=1),
            Pin(num='2',name='Pin_2',func=pin_types.PASSIVE,unit=1),
            Pin(num='3',name='Pin_3',func=pin_types.PASSIVE,unit=1),
            Pin(num='4',name='Pin_4',func=pin_types.PASSIVE,unit=1),
            Pin(num='5',name='Pin_5',func=pin_types.PASSIVE,unit=1),
            Pin(num='6',name='Pin_6',func=pin_types.PASSIVE,unit=1),
            Pin(num='7',name='Pin_7',func=pin_types.PASSIVE,unit=1),
            Pin(num='8',name='Pin_8',func=pin_types.PASSIVE,unit=1),
            Pin(num='9',name='Pin_9',func=pin_types.PASSIVE,unit=1),
            Pin(num='10',name='Pin_10',func=pin_types.PASSIVE,unit=1),
            Pin(num='11',name='Pin_11',func=pin_types.PASSIVE,unit=1),
            Pin(num='12',name='Pin_12',func=pin_types.PASSIVE,unit=1),
            Pin(num='13',name='Pin_13',func=pin_types.PASSIVE,unit=1),
            Pin(num='14',name='Pin_14',func=pin_types.PASSIVE,unit=1),
            Pin(num='15',name='Pin_15',func=pin_types.PASSIVE,unit=1),
            Pin(num='16',name='Pin_16',func=pin_types.PASSIVE,unit=1),
            Pin(num='17',name='Pin_17',func=pin_types.PASSIVE,unit=1),
            Pin(num='18',name='Pin_18',func=pin_types.PASSIVE,unit=1),
            Pin(num='19',name='Pin_19',func=pin_types.PASSIVE,unit=1),
            Pin(num='20',name='Pin_20',func=pin_types.PASSIVE,unit=1),
            Pin(num='21',name='Pin_21',func=pin_types.PASSIVE,unit=1),
            Pin(num='22',name='Pin_22',func=pin_types.PASSIVE,unit=1),
            Pin(num='23',name='Pin_23',func=pin_types.PASSIVE,unit=1),
            Pin(num='24',name='Pin_24',func=pin_types.PASSIVE,unit=1),
            Pin(num='25',name='Pin_25',func=pin_types.PASSIVE,unit=1),
            Pin(num='26',name='Pin_26',func=pin_types.PASSIVE,unit=1),
            Pin(num='27',name='Pin_27',func=pin_types.PASSIVE,unit=1),
            Pin(num='28',name='Pin_28',func=pin_types.PASSIVE,unit=1),
            Pin(num='29',name='Pin_29',func=pin_types.PASSIVE,unit=1),
            Pin(num='30',name='Pin_30',func=pin_types.PASSIVE,unit=1),
            Pin(num='31',name='Pin_31',func=pin_types.PASSIVE,unit=1),
            Pin(num='32',name='Pin_32',func=pin_types.PASSIVE,unit=1),
            Pin(num='33',name='Pin_33',func=pin_types.PASSIVE,unit=1),
            Pin(num='34',name='Pin_34',func=pin_types.PASSIVE,unit=1),
            Pin(num='35',name='Pin_35',func=pin_types.PASSIVE,unit=1),
            Pin(num='36',name='Pin_36',func=pin_types.PASSIVE,unit=1),
            Pin(num='37',name='Pin_37',func=pin_types.PASSIVE,unit=1),
            Pin(num='38',name='Pin_38',func=pin_types.PASSIVE,unit=1),
            Pin(num='39',name='Pin_39',func=pin_types.PASSIVE,unit=1),
            Pin(num='40',name='Pin_40',func=pin_types.PASSIVE,unit=1)], 'unit_defs':[] })])
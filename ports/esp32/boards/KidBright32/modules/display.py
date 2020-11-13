# Original C++ code from https://gitlab.com/kidbright/kidbright32/-/blob/master/kidbright32/src/ht16k33.cpp
# Port & Dev to MicroPython by Sonthaya Nongnuch

from time import sleep
from machine import Pin, I2C

i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

HT16K33_ADDR          = const(0x70)

HT16K33_OSC_OFF       = const(0x20)
HT16K33_OSC_ON        = const(0x21)
HT16K33_DISP_OFF      = const(0x80)
HT16K33_DISP_ON       = const(0x81)
HT16K33_DIM_SET_8_16  = const(0xe7)
HT16K33_DIM_SET_16_16 = const(0xef)
HT16K33_DISP_ADDR_PTR = const(0x00)

ht16k33_ptr_conv = (0, 2, 4, 6, 8, 10, 12, 14, 1, 3, 5, 7, 9, 11, 13, 15)

font_6_8 = bytes([
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 0x00
    0x00, 0x7c, 0xa2, 0x8a, 0xa2, 0x7c,  # 0x01
    0x00, 0x7c, 0xd6, 0xf6, 0xd6, 0x7c,  # 0x02
    0x00, 0x38, 0x7c, 0x3e, 0x7c, 0x38,  # 0x03
    0x00, 0x18, 0x3c, 0x7e, 0x3c, 0x18,  # 0x04
    0x00, 0x0c, 0x6c, 0xfe, 0x6c, 0x0c,  # 0x05
    0x00, 0x18, 0x3a, 0x7e, 0x3a, 0x18,  # 0x06
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 0x07
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 0x08
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 0x09
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 0x0a
    0x00, 0x0c, 0x12, 0x52, 0x6c, 0x70,  # 0x0b
    0x00, 0x60, 0x94, 0x9e, 0x94, 0x60,  # 0x0c
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 0x0d
    0x00, 0x06, 0x7e, 0x50, 0xac, 0xfc,  # 0x0e
    0x00, 0x54, 0x38, 0x6c, 0x38, 0x54,  # 0x0f
    0x00, 0x00, 0xfe, 0x7c, 0x38, 0x10,  # 0x10
    0x00, 0x10, 0x38, 0x7c, 0xfe, 0x00,  # 0x11
    0x00, 0x28, 0x6c, 0xfe, 0x6c, 0x28,  # 0x12
    0x00, 0x00, 0xfa, 0x00, 0xfa, 0x00,  # 0x13
    0x00, 0x60, 0x90, 0xfe, 0x80, 0xfe,  # 0x14
    0x00, 0x44, 0xb2, 0xaa, 0x9a, 0x44,  # 0x15
    0x00, 0x06, 0x06, 0x06, 0x06, 0x00,  # 0x16
    0x00, 0x28, 0x6d, 0xff, 0x6d, 0x28,  # 0x17
    0x00, 0x20, 0x60, 0xfe, 0x60, 0x20,  # 0x18
    0x00, 0x08, 0x0c, 0xfe, 0x0c, 0x08,  # 0x19
    0x00, 0x10, 0x10, 0x7c, 0x38, 0x10,  # 0x1a
    0x00, 0x10, 0x38, 0x7c, 0x10, 0x10,  # 0x1b
    0x00, 0x1e, 0x02, 0x02, 0x02, 0x02,  # 0x1c
    0x00, 0x10, 0x7c, 0x10, 0x7c, 0x10,  # 0x1d
    0x00, 0x0c, 0x3c, 0xfc, 0x3c, 0x0c,  # 0x1e
    0x00, 0xc0, 0xf0, 0xfc, 0xf0, 0xc0,  # 0x1f
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 0x20
    0x00, 0x00, 0x60, 0xfa, 0x60, 0x00,  # 0x21
    0x00, 0xe0, 0xc0, 0x00, 0xe0, 0xc0,  # 0x22
    0x00, 0x24, 0x7e, 0x24, 0x7e, 0x24,  # 0x23
    0x00, 0x24, 0xd4, 0x56, 0x48, 0x00,  # 0x24
    0x00, 0xc6, 0xc8, 0x10, 0x26, 0xc6,  # 0x25
    0x00, 0x6c, 0x92, 0x6a, 0x04, 0x0a,  # 0x26
    0x00, 0x00, 0xe0, 0xc0, 0x00, 0x00,  # 0x27
    0x00, 0x00, 0x7c, 0x82, 0x00, 0x00,  # 0x28
    0x00, 0x00, 0x82, 0x7c, 0x00, 0x00,  # 0x29
    0x00, 0x10, 0x7c, 0x38, 0x7c, 0x10,  # 0x2a
    0x00, 0x10, 0x10, 0x7c, 0x10, 0x10,  # 0x2b
    0x00, 0x00, 0x07, 0x06, 0x00, 0x00,  # 0x2c
    0x00, 0x10, 0x10, 0x10, 0x10, 0x10,  # 0x2d
    0x00, 0x00, 0x06, 0x06, 0x00, 0x00,  # 0x2e
    0x00, 0x04, 0x08, 0x10, 0x20, 0x40,  # 0x2f
    0x00, 0x7c, 0x8a, 0x92, 0xa2, 0x7c,  # 0x30
    0x00, 0x00, 0x42, 0xfe, 0x02, 0x00,  # 0x31
    0x00, 0x46, 0x8a, 0x92, 0x92, 0x62,  # 0x32
    0x00, 0x44, 0x92, 0x92, 0x92, 0x6c,  # 0x33
    0x00, 0x18, 0x28, 0x48, 0xfe, 0x08,  # 0x34
    0x00, 0xf4, 0x92, 0x92, 0x92, 0x8c,  # 0x35
    0x00, 0x3c, 0x52, 0x92, 0x92, 0x0c,  # 0x36
    0x00, 0x80, 0x8e, 0x90, 0xa0, 0xc0,  # 0x37
    0x00, 0x6c, 0x92, 0x92, 0x92, 0x6c,  # 0x38
    0x00, 0x60, 0x92, 0x92, 0x94, 0x78,  # 0x39
    0x00, 0x00, 0x36, 0x36, 0x00, 0x00,  # 0x3a
    0x00, 0x00, 0x37, 0x36, 0x00, 0x00,  # 0x3b
    0x00, 0x10, 0x28, 0x44, 0x82, 0x00,  # 0x3c
    0x00, 0x24, 0x24, 0x24, 0x24, 0x24,  # 0x3d
    0x00, 0x00, 0x82, 0x44, 0x28, 0x10,  # 0x3e
    0x00, 0x40, 0x80, 0x9a, 0x90, 0x60,  # 0x3f
    0x00, 0x7c, 0x82, 0xba, 0xaa, 0x78,  # 0x40
    0x00, 0x7e, 0x88, 0x88, 0x88, 0x7e,  # 0x41
    0x00, 0xfe, 0x92, 0x92, 0x92, 0x6c,  # 0x42
    0x00, 0x7c, 0x82, 0x82, 0x82, 0x44,  # 0x43
    0x00, 0xfe, 0x82, 0x82, 0x82, 0x7c,  # 0x44
    0x00, 0xfe, 0x92, 0x92, 0x92, 0x82,  # 0x45
    0x00, 0xfe, 0x90, 0x90, 0x90, 0x80,  # 0x46
    0x00, 0x7c, 0x82, 0x92, 0x92, 0x5e,  # 0x47
    0x00, 0xfe, 0x10, 0x10, 0x10, 0xfe,  # 0x48
    0x00, 0x00, 0x82, 0xfe, 0x82, 0x00,  # 0x49
    0x00, 0x0c, 0x02, 0x02, 0x02, 0xfc,  # 0x4a
    0x00, 0xfe, 0x10, 0x28, 0x44, 0x82,  # 0x4b
    0x00, 0xfe, 0x02, 0x02, 0x02, 0x02,  # 0x4c
    0x00, 0xfe, 0x40, 0x20, 0x40, 0xfe,  # 0x4d
    0x00, 0xfe, 0x40, 0x20, 0x10, 0xfe,  # 0x4e
    0x00, 0x7c, 0x82, 0x82, 0x82, 0x7c,  # 0x4f
    0x00, 0xfe, 0x90, 0x90, 0x90, 0x60,  # 0x50
    0x00, 0x7c, 0x82, 0x8a, 0x84, 0x7a,  # 0x51
    0x00, 0xfe, 0x90, 0x90, 0x98, 0x66,  # 0x52
    0x00, 0x64, 0x92, 0x92, 0x92, 0x4c,  # 0x53
    0x00, 0x80, 0x80, 0xfe, 0x80, 0x80,  # 0x54
    0x00, 0xfc, 0x02, 0x02, 0x02, 0xfc,  # 0x55
    0x00, 0xf8, 0x04, 0x02, 0x04, 0xf8,  # 0x56
    0x00, 0xfc, 0x02, 0x3c, 0x02, 0xfc,  # 0x57
    0x00, 0xc6, 0x28, 0x10, 0x28, 0xc6,  # 0x58
    0x00, 0xe0, 0x10, 0x0e, 0x10, 0xe0,  # 0x59
    0x00, 0x8e, 0x92, 0xa2, 0xc2, 0x00,  # 0x5a
    0x00, 0x00, 0xfe, 0x82, 0x82, 0x00,  # 0x5b
    0x00, 0x40, 0x20, 0x10, 0x08, 0x04,  # 0x5c
    0x00, 0x00, 0x82, 0x82, 0xfe, 0x00,  # 0x5d
    0x00, 0x20, 0x40, 0x80, 0x40, 0x20,  # 0x5e
    0x01, 0x01, 0x01, 0x01, 0x01, 0x01,  # 0x5f
    0x00, 0x00, 0xc0, 0xe0, 0x00, 0x00,  # 0x60
    0x00, 0x04, 0x2a, 0x2a, 0x2a, 0x1e,  # 0x61
    0x00, 0xfe, 0x22, 0x22, 0x22, 0x1c,  # 0x62
    0x00, 0x1c, 0x22, 0x22, 0x22, 0x04,  # 0x63 'c' = 0x00, 0x1c, 0x22, 0x22, 0x22, 0x14
    0x00, 0x1c, 0x22, 0x22, 0x22, 0xfe,  # 0x64
    0x00, 0x1c, 0x2a, 0x2a, 0x2a, 0x10,  # 0x65
    0x00, 0x10, 0x7e, 0x90, 0x90, 0x00,  # 0x66
    0x00, 0x18, 0x25, 0x25, 0x25, 0x3e,  # 0x67
    0x00, 0xfe, 0x20, 0x20, 0x1e, 0x00,  # 0x68
    0x00, 0x00, 0x00, 0x5e, 0x02, 0x00,  # 0x69 'i' = 0x00, 0x00, 0x00, 0xbe, 0x02, 0x00
    0x00, 0x02, 0x01, 0x21, 0xbe, 0x00,  # 0x6a
    0x00, 0xfe, 0x08, 0x14, 0x22, 0x00,  # 0x6b
    0x00, 0x00, 0x00, 0xfe, 0x02, 0x00,  # 0x6c
    0x00, 0x3e, 0x20, 0x18, 0x20, 0x1e,  # 0x6d
    0x00, 0x3e, 0x20, 0x20, 0x1e, 0x00,  # 0x6e
    0x00, 0x1c, 0x22, 0x22, 0x22, 0x1c,  # 0x6f
    0x00, 0x3f, 0x22, 0x22, 0x22, 0x1c,  # 0x70
    0x00, 0x1c, 0x22, 0x22, 0x22, 0x3f,  # 0x71
    0x00, 0x22, 0x1e, 0x22, 0x20, 0x10,  # 0x72
    0x00, 0x10, 0x2a, 0x2a, 0x2a, 0x04,  # 0x73
    0x00, 0x20, 0x7c, 0x22, 0x24, 0x00,  # 0x74
    0x00, 0x3c, 0x02, 0x04, 0x3e, 0x00,  # 0x75
    0x00, 0x38, 0x04, 0x02, 0x04, 0x38,  # 0x76
    0x00, 0x3c, 0x06, 0x0c, 0x06, 0x3c,  # 0x77
    0x00, 0x36, 0x08, 0x08, 0x36, 0x00,  # 0x78
    0x00, 0x39, 0x05, 0x06, 0x3c, 0x00,  # 0x79
    0x00, 0x26, 0x2a, 0x2a, 0x32, 0x00,  # 0x7a
    0x00, 0x10, 0x7c, 0x82, 0x82, 0x00,  # 0x7b
    0x00, 0x00, 0x00, 0xee, 0x00, 0x00,  # 0x7c
    0x00, 0x00, 0x82, 0x82, 0x7c, 0x10,  # 0x7d
    0x00, 0x40, 0x80, 0x40, 0x80, 0x00,  # 0x7e
    0x00, 0x3c, 0x64, 0xc4, 0x64, 0x3c,  # 0x7f
    0x00, 0x78, 0x85, 0x87, 0x84, 0x48,  # 0x80
    0x00, 0xbc, 0x02, 0x04, 0xbe, 0x00,  # 0x81
    0x00, 0x1c, 0x2a, 0x2a, 0xaa, 0x90,  # 0x82
    0x00, 0x04, 0xaa, 0xaa, 0xaa, 0x1e,  # 0x83
    0x00, 0x04, 0xaa, 0x2a, 0xaa, 0x1e,  # 0x84
    0x00, 0x04, 0xaa, 0xaa, 0x2a, 0x1e,  # 0x85
    0x00, 0x04, 0xea, 0xaa, 0xea, 0x1e,  # 0x86
    0x00, 0x38, 0x45, 0x47, 0x44, 0x28,  # 0x87
    0x00, 0x1c, 0xaa, 0xaa, 0xaa, 0x10,  # 0x88
    0x00, 0x1c, 0xaa, 0x2a, 0xaa, 0x10,  # 0x89
    0x00, 0x1c, 0xaa, 0xaa, 0x2a, 0x10,  # 0x8a
    0x00, 0x00, 0x80, 0x3e, 0x82, 0x00,  # 0x8b
    0x00, 0x00, 0x80, 0xbe, 0x82, 0x00,  # 0x8c
    0x00, 0x00, 0x80, 0x3e, 0x02, 0x00,  # 0x8d
    0x00, 0x0e, 0x94, 0x24, 0x94, 0x0e,  # 0x8e
    0x00, 0x1e, 0xf4, 0xa4, 0xf4, 0x1e,  # 0x8f
    0x00, 0x3e, 0x2a, 0x2a, 0xaa, 0xa2,  # 0x90
    0x00, 0x2c, 0x2a, 0x3e, 0x2a, 0x1a,  # 0x91
    0x00, 0x7e, 0x90, 0xfe, 0x92, 0x92,  # 0x92
    0x00, 0x1c, 0xa2, 0xa2, 0x9c, 0x00,  # 0x93
    0x00, 0x1c, 0xa2, 0x22, 0x9c, 0x00,  # 0x94
    0x00, 0x9c, 0xa2, 0x22, 0x1c, 0x00,  # 0x95
    0x00, 0x3c, 0x82, 0x84, 0xbe, 0x00,  # 0x96
    0x00, 0xbc, 0x82, 0x04, 0x3e, 0x00,  # 0x97
    0x00, 0x39, 0x85, 0x06, 0xbc, 0x00,  # 0x98
    0x00, 0xbc, 0x42, 0x42, 0xbc, 0x00,  # 0x99
    0x00, 0x3c, 0x82, 0x02, 0xbc, 0x00,  # 0x9a
    0x01, 0x0e, 0x16, 0x1a, 0x1c, 0x20,  # 0x9b
    0x00, 0x12, 0x7c, 0x92, 0x92, 0x46,  # 0x9c
    0x00, 0x7e, 0x86, 0xba, 0xc2, 0xfc,  # 0x9d
    0x00, 0x44, 0x28, 0x10, 0x28, 0x44,  # 0x9e
    0x00, 0x02, 0x11, 0x7e, 0x90, 0x40,  # 0x9f
    0x00, 0x04, 0x2a, 0xaa, 0xaa, 0x1e,  # 0xa0
    0x00, 0x00, 0x00, 0xbe, 0x82, 0x00,  # 0xa1
    0x00, 0x1c, 0x22, 0xa2, 0x9c, 0x00,  # 0xa2
    0x00, 0x3c, 0x02, 0x84, 0xbe, 0x00,  # 0xa3
    0x00, 0x5e, 0x90, 0x50, 0x8e, 0x00,  # 0xa4
    0x00, 0x5e, 0x88, 0x44, 0x9e, 0x00,  # 0xa5
    0x00, 0x10, 0xaa, 0xaa, 0xaa, 0x7a,  # 0xa6
    0x00, 0x72, 0x8a, 0x8a, 0x72, 0x00,  # 0xa7
    0x00, 0x0c, 0x12, 0xb2, 0x02, 0x04,  # 0xa8
    0x7c, 0x82, 0xba, 0xd2, 0xaa, 0x7c,  # 0xa9
    0x20, 0x20, 0x20, 0x20, 0x20, 0x38,  # 0xaa
    0x00, 0xe8, 0x10, 0x32, 0x56, 0x0a,  # 0xab
    0x00, 0xe8, 0x10, 0x2c, 0x54, 0x1e,  # 0xac
    0x00, 0x00, 0x0c, 0xbe, 0x0c, 0x00,  # 0xad
    0x00, 0x10, 0x28, 0x00, 0x10, 0x28,  # 0xae
    0x00, 0x28, 0x10, 0x00, 0x28, 0x10,  # 0xaf
    0x22, 0x88, 0x22, 0x88, 0x22, 0x88,  # 0xb0
    0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa,  # 0xb1
    0xdd, 0x77, 0xdd, 0x77, 0xdd, 0x77,  # 0xb2
    0x00, 0x00, 0x00, 0xff, 0x00, 0x00,  # 0xb3
    0x10, 0x10, 0x10, 0xff, 0x00, 0x00,  # 0xb4
    0x00, 0x0e, 0x14, 0xa4, 0x94, 0x0e,  # 0xb5
    0x00, 0x0e, 0x94, 0xa4, 0x94, 0x0e,  # 0xb6
    0x00, 0x0e, 0x94, 0xa4, 0x14, 0x0e,  # 0xb7
    0x7c, 0x82, 0xba, 0xaa, 0x82, 0x7c,  # 0xb8
    0x50, 0xdf, 0x00, 0xff, 0x00, 0x00,  # 0xb9
    0x00, 0xff, 0x00, 0xff, 0x00, 0x00,  # 0xba
    0x50, 0x5f, 0x40, 0x7f, 0x00, 0x00,  # 0xbb
    0x50, 0xd0, 0x10, 0xf0, 0x00, 0x00,  # 0xbc
    0x00, 0x18, 0x24, 0x66, 0x24, 0x00,  # 0xbd
    0x00, 0x94, 0x54, 0x3e, 0x54, 0x94,  # 0xbe
    0x10, 0x10, 0x10, 0x1f, 0x00, 0x00,  # 0xbf
    0x00, 0x00, 0x00, 0xf0, 0x10, 0x10,  # 0xc0
    0x10, 0x10, 0x10, 0xf0, 0x10, 0x10,  # 0xc1
    0x10, 0x10, 0x10, 0x1f, 0x10, 0x10,  # 0xc2
    0x00, 0x00, 0x00, 0xff, 0x10, 0x10,  # 0xc3
    0x10, 0x10, 0x10, 0x10, 0x10, 0x10,  # 0xc4
    0x10, 0x10, 0x10, 0xff, 0x10, 0x10,  # 0xc5
    0x00, 0x04, 0x6a, 0xaa, 0x6a, 0x9e,  # 0xc6
    0x00, 0x0e, 0x54, 0xa4, 0x54, 0x8e,  # 0xc7
    0x00, 0xf0, 0x10, 0xd0, 0x50, 0x50,  # 0xc8
    0x00, 0x7f, 0x40, 0x5f, 0x50, 0x50,  # 0xc9
    0x50, 0xd0, 0x10, 0xd0, 0x50, 0x50,  # 0xca
    0x50, 0x5f, 0x40, 0x5f, 0x50, 0x50,  # 0xcb
    0x00, 0xff, 0x00, 0xdf, 0x50, 0x50,  # 0xcc
    0x50, 0x50, 0x50, 0x50, 0x50, 0x50,  # 0xcd
    0x50, 0xdf, 0x00, 0xdf, 0x50, 0x50,  # 0xce
    0x00, 0xba, 0x44, 0x44, 0x44, 0xba,  # 0xcf
    0x00, 0x44, 0xaa, 0x9a, 0x0c, 0x00,  # 0xd0
    0x00, 0x10, 0xfe, 0x92, 0x82, 0x7c,  # 0xd1
    0x00, 0x3e, 0xaa, 0xaa, 0xaa, 0x22,  # 0xd2
    0x00, 0x3e, 0xaa, 0x2a, 0xaa, 0x22,  # 0xd3
    0x00, 0x3e, 0xaa, 0xaa, 0x2a, 0x22,  # 0xd4
    0x00, 0x00, 0x00, 0xe0, 0x00, 0x00,  # 0xd5
    0x00, 0x00, 0x22, 0xbe, 0xa2, 0x00,  # 0xd6
    0x00, 0x00, 0xa2, 0xbe, 0xa2, 0x00,  # 0xd7
    0x00, 0x00, 0xa2, 0x3e, 0xa2, 0x00,  # 0xd8
    0x10, 0x10, 0x10, 0xf0, 0x00, 0x00,  # 0xd9
    0x00, 0x00, 0x00, 0x1f, 0x10, 0x10,  # 0xda
    0xff, 0xff, 0xff, 0xff, 0xff, 0xff,  # 0xdb
    0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f,  # 0xdc
    0x00, 0x00, 0x00, 0xee, 0x00, 0x00,  # 0xdd
    0x00, 0x00, 0xa2, 0xbe, 0x22, 0x00,  # 0xde
    0xf0, 0xf0, 0xf0, 0xf0, 0xf0, 0xf0,  # 0xdf
    0x00, 0x3c, 0x42, 0xc2, 0xbc, 0x00,  # 0xe0
    0x00, 0x7f, 0x52, 0x52, 0x2c, 0x00,  # 0xe1
    0x00, 0x3c, 0xc2, 0xc2, 0xbc, 0x00,  # 0xe2
    0x00, 0xbc, 0xc2, 0x42, 0x3c, 0x00,  # 0xe3
    0x00, 0x4c, 0x92, 0x52, 0x8c, 0x00,  # 0xe4
    0x00, 0x5c, 0xa2, 0x62, 0x9c, 0x00,  # 0xe5
    0x00, 0x3f, 0x04, 0x04, 0x38, 0x00,  # 0xe6
    0x00, 0x7f, 0x55, 0x14, 0x08, 0x00,  # 0xe7
    0x00, 0xff, 0xa5, 0x24, 0x18, 0x00,  # 0xe8
    0x00, 0x3c, 0x02, 0x82, 0xbc, 0x00,  # 0xe9
    0x00, 0x3c, 0x82, 0x82, 0xbc, 0x00,  # 0xea
    0x00, 0xbc, 0x82, 0x02, 0x3c, 0x00,  # 0xeb
    0x00, 0x39, 0x05, 0x86, 0xbc, 0x00,  # 0xec
    0x00, 0x20, 0x10, 0x8e, 0x90, 0x20,  # 0xed
    0x00, 0x00, 0x40, 0x40, 0x40, 0x00,  # 0xee
    0x00, 0x00, 0xe0, 0xc0, 0x00, 0x00,  # 0xef
    0x00, 0x00, 0x10, 0x10, 0x10, 0x00,  # 0xf0
    0x00, 0x00, 0x24, 0x74, 0x24, 0x00,  # 0xf1
    0x00, 0x24, 0x24, 0x24, 0x24, 0x24,  # 0xf2
    0xa0, 0xe8, 0x50, 0x2c, 0x54, 0x1e,  # 0xf3
    0x00, 0x60, 0x90, 0xfe, 0x80, 0xfe,  # 0xf4
    0x00, 0x44, 0xb2, 0xaa, 0x9a, 0x44,  # 0xf5
    0x00, 0x10, 0x10, 0x54, 0x10, 0x10,  # 0xf6
    0x00, 0x00, 0x10, 0x18, 0x18, 0x00,  # 0xf7
    0x00, 0x60, 0x90, 0x90, 0x60, 0x00,  # 0xf8
    0x00, 0x00, 0x10, 0x00, 0x10, 0x00,  # 0xf9
    0x00, 0x00, 0x10, 0x00, 0x00, 0x00,  # 0xfa
    0x00, 0x40, 0xf0, 0x00, 0x00, 0x00,  # 0xfb
    0x00, 0x90, 0xf0, 0xa0, 0x00, 0x00,  # 0xfc
    0x00, 0x90, 0xb0, 0x50, 0x00, 0x00,  # 0xfd
    0x00, 0x3c, 0x3c, 0x3c, 0x3c, 0x00,  # 0xfe
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00  # 0xff
])

font4x8 = bytes([
    0x00, 0x7c, 0x44, 0x7c, # 0
    0x00, 0x00, 0x7c, 0x00, # 1
    0x00, 0x5c, 0x54, 0x74, # 2
    0x00, 0x54, 0x54, 0x7c, # 3
    0x00, 0x70, 0x10, 0x7c, # 4
    0x00, 0x74, 0x54, 0x5c, # 5
    0x00, 0x7c, 0x54, 0x5c, # 6
    0x00, 0x40, 0x40, 0x7c, # 7
    0x00, 0x7c, 0x54, 0x7c, # 8
    0x00, 0x74, 0x54, 0x7c, # 9
    0x00, 0x3c, 0x50, 0x3c, # A
    0x00, 0x7c, 0x54, 0x38, # B
    0x00, 0x38, 0x44, 0x44, # C
    0x00, 0x7c, 0x44, 0x38, # D
    0x00, 0x7c, 0x54, 0x54, # E
    0x00, 0x7c, 0x50, 0x50, # F
    0x00, 0x10, 0x10, 0x10, # -
    0x00, 0x00, 0x00, 0x00
])

displayBuff = bytearray(16)

def raw(data):
    buffer = bytearray(17)
    buffer[0] = HT16K33_DISP_ADDR_PTR
    for i in range(16):
        buffer[ht16k33_ptr_conv[i] + 1] = data[i]
    i2c0.writeto(HT16K33_ADDR, buffer)

def show(value):
    value = str(value)
    value = bytearray(value)
    value = value[-2:] # limit only 2-char
    buffer = bytearray(16)
    buffer[0] = 0
    buffer[1] = 0
    buffer[2] = 0
    buffer[3] = 0
    if (len(value) >= 2):
        for i in range(6):
            buffer[i + 4] = font_6_8[((value[0] * 6) + i)]
        for i in range(6):
            buffer[i + 4 + 6] = font_6_8[((value[1] * 6) + i)]
    else:
        for i in range(6):
            buffer[i + 4] = 0
        for i in range(6):
            buffer[i + 4 + 6] = font_6_8[((value[0] * 6) + i)]
    raw(buffer)


def scroll(value, speed=0.06):
    value = str(value)
    value = bytearray(value)
    buffer = bytearray(16 + (len(value) * 6) + 16)
    for i in range(16):
        buffer[i] = 0
    for x in range(len(value)):
        for i in range(6):
            buffer[i + 16 + (x * 6)] = font_6_8[((value[x] * 6) + i)]
    for i in range(16):
        buffer[16 + (len(value) * 6) + i] = 0
    for i in range(16 + (len(value) * 6)):
        raw(buffer[i:(i+16)])
        sleep(speed)
    clear()


def clear():
    global displayBuff
    raw(b'\x00' * 16)
    displayBuff = bytearray(16)

def show4x8(value):
    value = str(value).upper()
    value = bytearray(value)
    value = value[:5]
    value = value[:(5 if b'.' in value else 4)]
    buffer = bytearray(16)
    nextIndex = 0
    if (len(value) < (5 if b'.' in value else 4)): # fit to right
        nextIndex = nextIndex + (((5 if b'.' in value else 4) - len(value)) * 4)
    showDotFlag = False
    for x in range(len(value)):
        c = value[x]
        charIndex = 0
        if c >= ord(b'0') and c <= ord(b'9'):
            charIndex = c - ord(b'0')
        elif c >= ord(b'a') and c <= ord(b'f'):
            charIndex = c - ord(b'a') + 10
        elif c == ord(b'-'):
            charIndex = 16
        elif c == ord(b'.'):
            showDotFlag = True
            continue
        else:
            nextIndex = nextIndex + 4
            continue
        for i in range(4):
            buffer[nextIndex] = font4x8[((charIndex * 4) + i)] | (0x04 if showDotFlag else 0)
            if showDotFlag: 
                showDotFlag = False
            nextIndex = nextIndex + 1
    raw(buffer)

def left(value):
    global displayBuff
    def getCharIndex(c):
        if c >= ord(b'0') and c <= ord(b'9'):
            return c - ord(b'0')
        elif c >= ord(b'a') and c <= ord(b'f'):
            return c - ord(b'a') + 10
        elif c == ord(b'-'):
            return 16
        else:
            return 17
    value = int(value)
    value = str(value).upper()
    value = bytearray(value)
    value = value[:2]
    if len(value) == 1:
        charIndex = getCharIndex(value[0])
        displayBuff[0] = 0x00
        displayBuff[1] = 0x00
        displayBuff[2] = 0x00
        displayBuff[3] = font4x8[(charIndex * 4) + 1]
        displayBuff[4] = font4x8[(charIndex * 4) + 2]
        displayBuff[5] = font4x8[(charIndex * 4) + 3]
        displayBuff[6] = 0x00
        displayBuff[7] = 0x00
    elif len(value) == 2:
        charIndex = getCharIndex(value[0])
        displayBuff[0] = font4x8[(charIndex * 4) + 1]
        displayBuff[1] = font4x8[(charIndex * 4) + 2]
        displayBuff[2] = font4x8[(charIndex * 4) + 3]
        displayBuff[3] = 0x00

        charIndex = getCharIndex(value[1])
        displayBuff[4] = font4x8[(charIndex * 4) + 1]
        displayBuff[5] = font4x8[(charIndex * 4) + 2]
        displayBuff[6] = font4x8[(charIndex * 4) + 3]
        displayBuff[7] = 0x00
    raw(displayBuff)

def right(value):
    global displayBuff
    def getCharIndex(c):
        if c >= ord(b'0') and c <= ord(b'9'):
            return c - ord(b'0')
        elif c >= ord(b'a') and c <= ord(b'f'):
            return c - ord(b'a') + 10
        elif c == ord(b'-'):
            return 16
        else:
            return 17
    value = int(value)
    value = str(value).upper()
    value = bytearray(value)
    value = value[:2]
    if len(value) == 1:
        charIndex = getCharIndex(value[0])
        displayBuff[8] = 0x00
        displayBuff[9] = 0x00
        displayBuff[10] = 0x00
        displayBuff[11] = font4x8[(charIndex * 4) + 1]
        displayBuff[12] = font4x8[(charIndex * 4) + 2]
        displayBuff[13] = font4x8[(charIndex * 4) + 3]
        displayBuff[14] = 0x00
        displayBuff[15] = 0x00
    elif len(value) == 2:
        charIndex = getCharIndex(value[0])
        displayBuff[8] = 0x00
        displayBuff[9] = font4x8[(charIndex * 4) + 1]
        displayBuff[10] = font4x8[(charIndex * 4) + 2]
        displayBuff[11] = font4x8[(charIndex * 4) + 3]

        charIndex = getCharIndex(value[1])
        displayBuff[12] = 0x00
        displayBuff[13] = font4x8[(charIndex * 4) + 1]
        displayBuff[14] = font4x8[(charIndex * 4) + 2]
        displayBuff[15] = font4x8[(charIndex * 4) + 3]
    raw(displayBuff)

def plot(value):
    global displayBuff
    displayBuff = displayBuff[-15:] + b'\x00'
    value = int(value)
    if value >= 0 and value <= 7:
        displayBuff[15] = 0x01 << int(value)
    else:
        displayBuff[15] = 0
    raw(displayBuff)

clear()
i2c0.writeto(HT16K33_ADDR, bytes([ HT16K33_OSC_ON ]))
i2c0.writeto(HT16K33_ADDR, bytes([ HT16K33_DIM_SET_8_16 ]))
i2c0.writeto(HT16K33_ADDR, bytes([ HT16K33_DISP_ON ]))
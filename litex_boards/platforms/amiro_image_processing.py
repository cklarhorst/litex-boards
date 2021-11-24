# Support for the Digilent Atlys (http://digilentinc.com/atlys/) - The board used for HDMI2USB prototyping.

from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform, iMPACT

LVCMOS_BANK0="LVTTL"
LVCMOS_BANK1="LVTTL"
LVCMOS_BANK2="LVTTL"
LVCMOS_BANK3="LVTTL"

_io = [
    # NET "clk"   LOC = "L15"; # Bank = 1, Pin name = IO_L42P_GCLK7_M1UDM, Type = GCLK, Sch name = GCLK
    # SG8002JF - 100MHz - CMOS Crystal Oscillator
    ("clk100", 0, Pins("AB13"), IOStandard(LVCMOS_BANK1)), # checked 100mhz

    # M0/RESET button
    #  VCCB2 --[10K]--+--[1k]-- M0/Reset
    #                 |
    #    GND -[ BTN ]-+--[390]- BTNRST
    # NET "btn<0>" LOC = "T15"; # Bank = 2, Pin name = IO_L1N_M0_CMPMISO_2,    Sch name = M0/RESET
    ("cpu_reset", 0, Pins("B22"), IOStandard(LVCMOS_BANK2)), # MODIFIED

    ## onBoard USB controller - FIXME
    # CY7C68013A-56
    # EEPROM config 24AA128 -- A0,A1,A2 = 1,0,0 -- JP9 connects / disconnects SDA
    # NET "EppAstb"   LOC = "B9";  # Bank = 0, Pin name = IO_L35P_GCLK17, Sch name = U1-FLAGA
    # NET "EppDstb"   LOC = "A9";  # Bank = 0, Pin name = IO_L35N_GCLK16, Sch name = U1-FLAGB
    # NET "UsbFlag"   LOC = "C15"; # Bank = 0, Pin name = IO_L64P_SCP5,   Sch name = U1-FLAGC
    # NET "EppWait"   LOC = "F13"; # Bank = 0, Pin name = IO_L63P_SCP7,   Sch name = U1-SLRD
    # NET "EppDB<0>"  LOC = "A2";  # Bank = 0, Pin name = IO_L2N,         Sch name = U1-FD0
    # NET "EppDB<1>"  LOC = "D6";  # Bank = 0, Pin name = IO_L3P,         Sch name = U1-FD1
    # NET "EppDB<2>"  LOC = "C6";  # Bank = 0, Pin name = IO_L3N,         Sch name = U1-FD2
    # NET "EppDB<3>"  LOC = "B3";  # Bank = 0, Pin name = IO_L4P,         Sch name = U1-FD3
    # NET "EppDB<4>"  LOC = "A3";  # Bank = 0, Pin name = IO_L4N,         Sch name = U1-FD4
    # NET "EppDB<5>"  LOC = "B4";  # Bank = 0, Pin name = IO_L5P,         Sch name = U1-FD5
    # NET "EppDB<6>"  LOC = "A4";  # Bank = 0, Pin name = IO_L5N,         Sch name = U1-FD6
    # NET "EppDB<7>"  LOC = "C5";  # Bank = 0, Pin name = IO_L6P,         Sch name = U1-FD7

    # HDMI2USB configuration....
    ("fx2", 0,
        Subsignal("ifclk", Pins("C10")),
        Subsignal("data", Pins("A2 D6 C6 B3 A3 B4 A4 C5")),
        Subsignal("addr", Pins("A14 B14"), Misc("DRIVE=12")),
        Subsignal("flaga", Pins("B9"), Misc("DRIVE=12")),
        Subsignal("flagb", Pins("A9"), Misc("DRIVE=12")),
        Subsignal("flagc", Pins("C15"), Misc("DRIVE=12")),
        Subsignal("rd_n", Pins("F13"), Misc("DRIVE=12")),
        Subsignal("wr_n", Pins("E13")),
        Subsignal("oe_n", Pins("A15"), Misc("DRIVE=12")),
        Subsignal("cs_n", Pins("B2")),
        Subsignal("pktend_n", Pins("C4"), Misc("DRIVE=12")),
        IOStandard(LVCMOS_BANK0)
    ),

    ## onBoard Quad-SPI Flash
    # 16Mbyte x4 SPI Flash for configuration & data storage. An FPGA
    # configuration file requires less than 12Mbits, leaving 116Mbits
    # available for user data.
    # Numonyx -- N25Q12-F8 or N25Q12-SF
    # DQ0 - SDI, DQ1 - SDO, DQ2 -> ^WP/DQ2 (pulled high), DQ3 -> ^HOLD/DQ3 (pulled high)
    ("spiflash", 0,
        Subsignal("cs_n", Pins("Y15"), IOStandard("LVCMOS33")),
        Subsignal("clk",  Pins("Y21"), IOStandard("LVCMOS33")),
        Subsignal("mosi", Pins("AB20"), IOStandard("LVCMOS33")),
        Subsignal("miso", Pins("AA20"), IOStandard("LVCMOS33"))
    ),

    ## onBoard Leds
    # NET "Led<0>" LOC = "U18"; # Bank = 1, Pin name = IO_L52N_M1DQ15,       Sch name = LD0
    # NET "Led<1>" LOC = "M14"; # Bank = 1, Pin name = IO_L53P,              Sch name = LD1
    # NET "Led<2>" LOC = "N14"; # Bank = 1, Pin name = IO_L53N_VREF,         Sch name = LD2
    # NET "Led<3>" LOC = "L14"; # Bank = 1, Pin name = IO_L61P,              Sch name = LD3
    # NET "Led<4>" LOC = "M13"; # Bank = 1, Pin name = IO_L61N,              Sch name = LD4
    # NET "Led<5>" LOC = "D4";  # Bank = 0, Pin name = IO_L1P_HSWAPEN_0,     Sch name = HSWAP/LD5
    # NET "Led<6>" LOC = "P16"; # Bank = 1, Pin name = IO_L74N_DOUT_BUSY_1,  Sch name = LD6
    # NET "Led<7>" LOC = "N12"; # Bank = 2, Pin name = IO_L13P_M1_2,         Sch name = M1/LD7
    ("user_led", 0, Pins("U18"), IOStandard(LVCMOS_BANK1)),
    ("user_led", 1, Pins("M14"), IOStandard(LVCMOS_BANK1)),
    ("user_led", 2, Pins("N14"), IOStandard(LVCMOS_BANK1)),
    ("user_led", 3, Pins("L14"), IOStandard(LVCMOS_BANK1)),
    ("user_led", 4, Pins("M13"), IOStandard(LVCMOS_BANK1)),
    ("user_led", 5, Pins("D4"),  IOStandard(LVCMOS_BANK0)),
    ("user_led", 6, Pins("P16"), IOStandard(LVCMOS_BANK1)),
    ("user_led", 7, Pins("N12"), IOStandard(LVCMOS_BANK2)),

    ## onBoard PUSH BUTTONS - FIXME
    # Mapping "up" to north
    # VCC1V8 - pulled down to GND via 10k
    # NET "btn<1>" LOC = "N4";  # Bank = 3, Pin name = IO_L1P,               Sch name = BTNU
    ("user_btn", 0, Pins("N4"), IOStandard(LVCMOS_BANK3)), # North button
    # NET "btn<2>" LOC = "P4";  # Bank = 3, Pin name = IO_L2P,               Sch name = BTNL
    ("user_btn", 1, Pins("P4"), IOStandard(LVCMOS_BANK3)), # East button
    # NET "btn<3>" LOC = "P3";  # Bank = 3, Pin name = IO_L2N,               Sch name = BTND
    ("user_btn", 2, Pins("P3"), IOStandard(LVCMOS_BANK3)), # South button
    # NET "btn<4>" LOC = "F6";  # Bank = 3, Pin name = IO_L55P_M3A13,        Sch name = BTNR
    ("user_btn", 3, Pins("F6"), IOStandard(LVCMOS_BANK3)), # West button
    # NET "btn<5>" LOC = "F5";  # Bank = 3, Pin name = IO_L55N_M3A14,        Sch name = BTNC
    ("user_btn", 4, Pins("F5"), IOStandard(LVCMOS_BANK3)), # Center button

    ## onBoard SWITCHES - FIXME
    # SW(0,1,2,3) - VCC3V3 / GND
    # SW(4,5,6) - VCCB2 / GND
    # SW(7) - VCC1V8 / GND
    # NET "sw<0>" LOC = "A10"; # Bank = 0, Pin name = IO_L37N_GCLK12,         Sch name = SW0
    # NET "sw<1>" LOC = "D14"; # Bank = 0, Pin name = IO_L65P_SCP3,           Sch name = SW1
    # NET "sw<2>" LOC = "C14"; # Bank = 0, Pin name = IO_L65N_SCP2,           Sch name = SW2
    # NET "sw<3>" LOC = "P15"; # Bank = 1, Pin name = IO_L74P_AWAKE_1,        Sch name = SW3
    # NET "sw<4>" LOC = "P12"; # Bank = 2, Pin name = IO_L13N_D10,            Sch name = SW4
    # NET "sw<5>" LOC = "R5";  # Bank = 2, Pin name = IO_L48P_D7,             Sch name = SW5
    # NET "sw<6>" LOC = "T5";  # Bank = 2, Pin name = IO_L48N_RDWR_B_VREF_2,  Sch name = SW6
    # NET "sw<7>" LOC = "E4";  # Bank = 3, Pin name = IO_L54P_M3RESET,        Sch name = SW7
    ("user_sw", 0, Pins("A10"), IOStandard(LVCMOS_BANK0)),
    ("user_sw", 1, Pins("D14"), IOStandard(LVCMOS_BANK0)),
    ("user_sw", 2, Pins("C14"), IOStandard(LVCMOS_BANK0)),
    ("user_sw", 3, Pins("P15"), IOStandard(LVCMOS_BANK1)),
    ("user_sw", 4, Pins("P12"), IOStandard(LVCMOS_BANK2)),
    ("user_sw", 5, Pins("R5"),  IOStandard(LVCMOS_BANK2)),
    ("user_sw", 6, Pins("T5"),  IOStandard(LVCMOS_BANK2)),
    ("user_sw", 7, Pins("E4"),  IOStandard(LVCMOS_BANK3)),

    ## TEMAC Ethernet MAC - FIXME
    # 10/100/1000 Ethernet PHY
    # 88E111-B2-RCJ1-C000 - Marvell Alaska Tri-mode PHY (the 88E1111)
    # paired with a Halo HFJ11-1G01E RJ-45 connector
    # Runs from 1.2V power supply
    ("eth_clocks", 0,
        # NET "phytxclk"  LOC = "K16"; # Bank = 1, Pin name = IO_L41N_GCLK8_M1CASN,       Sch name = E-TXCLK
        Subsignal("tx", Pins("K16")),
        # NET "phygtxclk" LOC = "L12"; # Bank = 1, Pin name = IO_L40P_GCLK11_M1A5,        Sch name = E-GTXCLK
        Subsignal("gtx", Pins("L12")),
        # NET "phyrxclk"  LOC = "K15"; # Bank = 1, Pin name = IO_L41P_GCLK9_IRDY1_M1RASN, Sch name = E-RXCLK
        Subsignal("rx", Pins("K15")),
        IOStandard(LVCMOS_BANK1)
    ),
    ("eth", 0,
        # NET "phyrst"    LOC = "G13"; # Bank = 1, Pin name = IO_L32N_A16_M1A9,    Sch name = E-RESET
        Subsignal("rst_n", Pins("G13")),
        # NET "phyint"    LOC = "L16"; # Bank = 1, Pin name = IO_L42N_GCLK6_TRDY1_M1LDM, Sch name = E-INT
        Subsignal("int_n", Pins("L16")),
        # NET "phymdi"    LOC = "N17"; # Bank = 1, Pin name = IO_L48P_HDC_M1DQ8,   Sch name = E-MDIO
        Subsignal("mdio", Pins("N17")),
        # NET "phymdc"    LOC = "F16"; # Bank = 1, Pin name = IO_L1N_A24_VREF,     Sch name = E-MDC
        Subsignal("mdc", Pins("F16")),
        # NET "phyrxdv"   LOC = "F17"; # Bank = 1, Pin name = IO_L35P_A11_M1A7,    Sch name = E-RXDV
        Subsignal("rx_dv", Pins("F17")),
        # NET "phyrxer"   LOC = "F18"; # Bank = 1, Pin name = IO_L35N_A10_M1A2,    Sch name = E-RXER
        Subsignal("rx_er", Pins("F18")),
        # NET "phyRXD<0>" LOC = "G16"; # Bank = 1, Pin name = IO_L38P_A5_M1CLK,    Sch name = E-RXD0
        # NET "phyRXD<1>" LOC = "H14"; # Bank = 1, Pin name = IO_L36N_A8_M1BA1,    Sch name = E-RXD1
        # NET "phyRXD<2>" LOC = "E16"; # Bank = 1, Pin name = IO_L33P_A15_M1A10,   Sch name = E-RXD2
        # NET "phyRXD<3>" LOC = "F15"; # Bank = 1, Pin name = IO_L1P_A25,          Sch name = E-RXD3
        # NET "phyRXD<4>" LOC = "F14"; # Bank = 1, Pin name = IO_L30P_A21_M1RESET, Sch name = E-RXD4
        # NET "phyRXD<5>" LOC = "E18"; # Bank = 1, Pin name = IO_L33N_A14_M1A4,    Sch name = E-RXD5
        # NET "phyRXD<6>" LOC = "D18"; # Bank = 1, Pin name = IO_L31N_A18_M1A12,   Sch name = E-RXD6
        # NET "phyRXD<7>" LOC = "D17"; # Bank = 1, Pin name = IO_L31P_A19_M1CKE,   Sch name = E-RXD7
        Subsignal("rx_data", Pins("G16 H14 E16 F15 F14 E18 D18 D17")),
        # NET "phytxen"   LOC = "H15"; # Bank = 1, Pin name = IO_L37P_A7_M1A0,     Sch name = E-TXEN
        Subsignal("tx_en", Pins("H15")),
        # NET "phytxer"   LOC = "G18"; # Bank = 1, Pin name = IO_L38N_A4_M1CLKN,   Sch name = E-TXER
        Subsignal("tx_er", Pins("G18")),
        # NET "phyTXD<0>" LOC = "H16"; # Bank = 1, Pin name = IO_L37N_A6_M1A1,     Sch name = E-TXD0
        # NET "phyTXD<1>" LOC = "H13"; # Bank = 1, Pin name = IO_L36P_A9_M1BA0,    Sch name = E-TXD1
        # NET "phyTXD<2>" LOC = "K14"; # Bank = 1, Pin name = IO_L39N_M1ODT,       Sch name = E-TXD2
        # NET "phyTXD<3>" LOC = "K13"; # Bank = 1, Pin name = IO_L34N_A12_M1BA2,   Sch name = E-TXD3
        # NET "phyTXD<4>" LOC = "J13"; # Bank = 1, Pin name = IO_L39P_M1A3,        Sch name = E-TXD4
        # NET "phyTXD<5>" LOC = "G14"; # Bank = 1, Pin name = IO_L30N_A20_M1A11,   Sch name = E-TXD5
        # NET "phyTXD<6>" LOC = "H12"; # Bank = 1, Pin name = IO_L32P_A17_M1A8,    Sch name = E-TXD6
        # NET "phyTXD<7>" LOC = "K12"; # Bank = 1, Pin name = IO_L34P_A13_M1WE,    Sch name = E-TXD7
        Subsignal("tx_data", Pins("H16 H13 K14 K13 J13 G14 H12 K12")),
        # C17 - from Atlys reference manual, not listed in UCF file?
        Subsignal("col", Pins("C17")),
        # C18 - from Atlys reference manual, not listed in UCF file?
        Subsignal("crs", Pins("C18")),
        IOStandard(LVCMOS_BANK1)
    ),

    ## DDR2
    # 128Mbyte DDR2 16-bit wide data @ 800MHz
    # Older boards - MT47H64M16HR-25E - DDR2 - 2.5ns @ CL = 5 (DDR2-800)
    # Newer boards - MIRA P3R1GE3EGF G8E DDR2 -
    #
    # The interface supports SSTL18 signaling. Address and control signals
    # are terminated through 47-ohm resistors to a 0.9V VTT, and data
    # signals use the On-Die-Termination (ODT) feature of the DDR2 chip.
    #
    # When generating a MIG core for the MIRA part, selecting the
    # “EDE1116AXXX-8E” device will result in the correct timing parameters
    # being set. When generating a component for the Micron part, it can be
    # selected by name within the wizard. The part loaded on your Atlys can
    # be determined by examining the print on the DDR2 component (IC13).
    #
    # NET "DDR2CLK0"   LOC = "G3"; # Bank = 3, Pin name = IO_L46P_M3CLK,               Sch name = DDR-CK_P DIFF_MOBILE_DDR
    # NET "DDR2CLK1"   LOC = "G1"; # Bank = 3, Pin name = IO_L46N_M3CLKN,              Sch name = DDR-CK_N MOBILE_DDR
    ("ddram_clock", 0,
        Subsignal("p", Pins("H20")),
        Subsignal("n", Pins("J19")),
        IOStandard("MOBILE_DDR") #IOStandard("DIFF_MOBILE_DDR"), Misc("SLEW=FAST"), Misc("DRIVE=24") #DIFF_MOBILE_DDR DIFF_MOBILE_DDR DIFF_SSTL18_II
    ),
    
    ("ddram", 0, #lpddr_dqs?
        Subsignal("a", Pins("F21 F22 E22 G20 F20 K20 K19 E20 C20 C22 G19 F19 D22 D19")),
        Subsignal("ba", Pins("J17 K17")),
        Subsignal("ras_n", Pins("H21")),
        Subsignal("cas_n", Pins("H22")),
        Subsignal("we_n", Pins("H19")),
        Subsignal("cs_n", Pins("H17")),
        Subsignal("dm", Pins("L19 M20")),  #was M20 L19
        Subsignal("dq", Pins("N20 N22 M21 M22 J20 J22 K21 K22 P21 P22 R20 R22 U20 U22 V21 V22")), #Misc("IN_TERM=UNTUNED_SPLIT_40")),
        Subsignal("dqs", Pins("L20 T21")),# was T21 ..
        #Subsignal("clk_p", Pins("H20"), IOStandard("DIFF_MOBILE_DDR")),
        #Subsignal("clk_n", Pins("J19"), IOStandard("DIFF_MOBILE_DDR")),
        Subsignal("cke", Pins("D21")),
        IOStandard("MOBILE_DDR") #IOStandard("MOBILE_DDR"), Misc("SLEW=FAST"), Misc("DRIVE=24")
    ),

    ## onboard HDMI OUT
    # Type A connector, marked as J2 on the board, next to the power connector.
    # Buffered / protected with TMDS141RHAR
    # NET "HDMIOUTCLKP" LOC = "B6"; # Bank = 0, Pin name = IO_L8P,         Sch name = TMDS-TX-CLK_P
    # NET "HDMIOUTCLKN" LOC = "A6"; # Bank = 0, Pin name = IO_L8N_VREF,    Sch name = TMDS-TX-CLK_N
    # NET "HDMIOUTD0P"  LOC = "D8"; # Bank = 0, Pin name = IO_L11P,        Sch name = TMDS-TX-0_P
    # NET "HDMIOUTD0N"  LOC = "C8"; # Bank = 0, Pin name = IO_L11N,        Sch name = TMDS-TX-0_N
    # NET "HDMIOUTD1P"  LOC = "C7"; # Bank = 0, Pin name = IO_L10P,        Sch name = TMDS-TX-1_P
    # NET "HDMIOUTD1N"  LOC = "A7"; # Bank = 0, Pin name = IO_L10N,        Sch name = TMDS-TX-1_N
    # NET "HDMIOUTD2P"  LOC = "B8"; # Bank = 0, Pin name = IO_L33P,        Sch name = TMDS-TX-2_P
    # NET "HDMIOUTD2N"  LOC = "A8"; # Bank = 0, Pin name = IO_L33N,        Sch name = TMDS-TX-2_N
    # NET "HDMIOUTSCL"  LOC = "D9"; # Bank = 0, Pin name = IO_L34P_GCLK19, Sch name = TMDS-TX-SCL
    # NET "HDMIOUTSDA"  LOC = "C9"; # Bank = 0, Pin name = IO_L34N_GCLK18, Sch name = TMDS-TX-SDA
    ("hdmi_out", 0,
        Subsignal("clk_p", Pins("B6"), IOStandard("TMDS_33")),
        Subsignal("clk_n", Pins("A6"), IOStandard("TMDS_33")),
        Subsignal("data0_p", Pins("D8"), IOStandard("TMDS_33")),
        Subsignal("data0_n", Pins("C8"), IOStandard("TMDS_33")),
        Subsignal("data1_p", Pins("C7"), IOStandard("TMDS_33")),
        Subsignal("data1_n", Pins("A7"), IOStandard("TMDS_33")),
        Subsignal("data2_p", Pins("B8"), IOStandard("TMDS_33")),
        Subsignal("data2_n", Pins("A8"), IOStandard("TMDS_33")),
        # Disconnect JP6 and JP7 for FPGA SCL/SDA control, otherwise
        # this is connected to J3's SCL/SDA pins.
        Subsignal("scl", Pins("D9"), IOStandard("I2C")),
        Subsignal("sda", Pins("C9"), IOStandard("I2C")),
    ),

    ## onboard HDMI IN1 (PMODA)
    # Type A connector, marked as J1, on side with USB connectors.
    # Buffered / protected with TMDS141RHAR
    # JP4 connects / disconnects 5V to HDMI pin 18, for input to work make
    # sure it is connected.
    # NET "HDMIIN1CLKP" LOC = "D11"; # Bank = 0, Pin name = IO_L36P_GCLK15, Sch name = TMDS-RXB-CLK_P
    # NET "HDMIIN1CLKN" LOC = "C11"; # Bank = 0, Pin name = IO_L36N_GCLK14, Sch name = TMDS-RXB-CLK_N
    # NET "HDMIIN1D0P"  LOC = "G9";  # Bank = 0, Pin name = IO_L38P,        Sch name = TMDS-RXB-0_P
    # NET "HDMIIN1D0N"  LOC = "F9";  # Bank = 0, Pin name = IO_L38N_VREF,   Sch name = TMDS-RXB-0_N
    # NET "HDMIIN1D1P"  LOC = "B11"; # Bank = 0, Pin name = IO_L39P,        Sch name = TMDS-RXB-1_P
    # NET "HDMIIN1D1N"  LOC = "A11"; # Bank = 0, Pin name = O_L39N,         Sch name = TMDS-RXB-1_N
    # NET "HDMIIN1D2P"  LOC = "B12"; # Bank = 0, Pin name = IO_L41P,        Sch name = TMDS-RXB-2_P
    # NET "HDMIIN1D2N"  LOC = "A12"; # Bank = 0, Pin name = IO_L41N,        Sch name = TMDS-RXB-2_N
    # NET "HDMIIN1SCL"  LOC = "C13"; # Bank = 0, Pin name = IO_L50P,        Sch name = PMOD-SCL
    # NET "HDMIIN1SDA"  LOC = "A13"; # Bank = 0, Pin name = IO_L50N,        Sch name = PMOD-SDA
    ("hdmi_in", 0,
        Subsignal("clk_p", Pins("D11")),
        Subsignal("clk_n", Pins("C11")),
        Subsignal("data0_p", Pins("G9")),
        Subsignal("data0_n", Pins("F9")),
        Subsignal("data1_p", Pins("B11")),
        Subsignal("data1_n", Pins("A11")),
        Subsignal("data2_p", Pins("B12")),
        Subsignal("data2_n", Pins("A12")),
        # Make sure JP2 is connected. Shared with J1.
        Subsignal("scl", Pins("C13"), IOStandard(LVCMOS_BANK0)),
        Subsignal("sda", Pins("A13"), IOStandard(LVCMOS_BANK0)),
        #Subsignal("hpd_notif", Pins("G22"), IOStandard("LVCMOS33")),
        #Subsignal("hpd_en", Pins("G17"), IOStandard("LVCMOS33"))
    ),

    ## onboard HDMI IN2
    # Type A connector, marked as J3, between audio connectors and Ethernet
    # RJ45 connector.
    # Buffered / protected with a TMDS141RHAR
    # JP8 connects / disconnects 5V to HDMI pin 18, for input to work make
    # sure it is connected.
    # NET "HDMIIN2CLKP" LOC = "H17"; # Bank = 1, Pin name = IO_L43P_GCLK5_M1DQ4, Sch name = TMDS-RX-CLK_P
    # NET "HDMIIN2CLKN" LOC = "H18"; # Bank = 1, Pin name = IO_L43N_GCLK4_M1DQ5, Sch name = TMDS-RX-CLK_N
    # NET "HDMIIN2D0P"  LOC = "K17"; # Bank = 1, Pin name = IO_L45P_A1_M1LDQS,   Sch name = TMDS-RX-0_P
    # NET "HDMIIN2D0N"  LOC = "K18"; # Bank = 1, Pin name = IO_L45N_A0_M1LDQSN,  Sch name = TMDS-RX-0_N
    # NET "HDMIIN2D1P"  LOC = "L17"; # Bank = 1, Pin name = IO_L46P_FCS_B_M1DQ2, Sch name = TMDS-RX-1_P
    # NET "HDMIIN2D1N"  LOC = "L18"; # Bank = 1, Pin name = IO_L46N_FOE_B_M1DQ3, Sch name = TMDS-RX-1_N
    # NET "HDMIIN2D2P"  LOC = "J16"; # Bank = 1, Pin name = IO_L44P_A3_M1DQ6,    Sch name = TMDS-RX-2_P
    # NET "HDMIIN2D2N"  LOC = "J18"; # Bank = 1, Pin name = IO_L44N_A2_M1DQ7,    Sch name = TMDS-RX-2_N
    # NET "HDMIIN2SCL"  LOC = "M16"; # Bank = 1, Pin name = IO_L47P_FWE_B_M1DQ0, Sch name = TMDS-RX-SCL
    # NET "HDMIIN2SDA"  LOC = "M18"; # Bank = 1, Pin name = IO_L47N_LDC_M1DQ1,   Sch name = TMDS-RX-SDA
    ("hdmi_in", 1,
        Subsignal("clk_p", Pins("H17")),
        Subsignal("clk_n", Pins("H18")),
        Subsignal("data0_p", Pins("K17")),
        Subsignal("data0_n", Pins("K18")),
        Subsignal("data1_p", Pins("L17")),
        Subsignal("data1_n", Pins("L18")),
        Subsignal("data2_p", Pins("J16")),
        Subsignal("data2_n", Pins("J18")),
        # Disconnect JP6 and JP7 for FPGA SCL/SDA control, otherwise
        # this is connected to J2's SCL/SDA pins.
        Subsignal("scl", Pins("M16"), IOStandard(LVCMOS_BANK1)),
        Subsignal("sda", Pins("M18"), IOStandard(LVCMOS_BANK1)),
        #Subsignal("hpd_notif", Pins("G16"), IOStandard("LVCMOS33")),
        #Subsignal("hpd_en", Pins("B20"), IOStandard("LVCMOS33"))
    ),
    ("sdcard", 0,
            Subsignal("data", Pins("AA4 Y3 AB4 AB3")),
            Subsignal("cmd",  Pins("AB2")),
            Subsignal("clk",  Pins("AA2")),
            Subsignal("cd",   Pins("AB6")),
            Misc("SLEW=FAST"),
            IOStandard("LVCMOS33"),
    ),
    ## onboard USB Host Controller - FIXME
    # PIC32MX440F256H-40I/MR
    # USB-HID port (for mouse/keyboard)
    # PS/2 Keyboard - K_CLK - P17
    # PS/2 Keyboard - K_DAT - N15
    # PS/2 Mouse - M_CLK - N18
    # PS/2 Mouse - M_DAT - P18
    # FPGA Serial programming - DIN - R13
    # FPGA Serial programming - CLK - R15
    # NET "USBCLK" LOC = "P17"; # Bank = 1, Pin name = IO_L49P_M1DQ10, Sch name = PIC32-SCK1
    # NET "USBSDI" LOC = "N15"; # Bank = 1, Pin name = IO_L50P_M1UDQS, Sch name = PIC32-SDI1

    # NET "USBSS"  LOC = "P18"; # Bank = 1, Pin name = IO_L49N_M1DQ11, Sch name = PIC32-SS1
    # NET "USBSDO" LOC = "N18"; # Bank = 1, Pin name = IO_L48N_M1DQ9,  Sch name = PIC32-SDO1

    ## Audio - FIXME
    # National Semiconductor - LM4550VH
    # AC-97 Codec with line-in, line-out, mic, & headphone
    # Audio
    # NET "BITCLK"   LOC = "L13"; # Bank = 1, Pin name = IO_L40N_GCLK10_M1A6, Sch name = AUD-BIT-CLK
    # NET "AUDSYNC"  LOC = "U17"; # Bank = 1, Pin name = IO_L52P_M1DQ14,      Sch name = AUD-SYNC
    # NET "AUDRST"   LOC = "T17"; # Bank = 1, Pin name = IO_L51P_M1DQ12,      Sch name = AUD-RESET
    # NET "AUDSDI"   LOC = "T18"; # Bank = 1, Pin name = IO_L51N_M1DQ13,      Sch name = AUD-SDI
    # NET "AUDSDO"   LOC = "N16"; # Bank = 1, Pin name = IO_L50N_M1UDQSN,     Sch name = AUD-SDO

    ## USB UART Connector
    # USB Micro B port marked as UART between HDMI connector and USB A connector.
    # XR21V1410IL16 - Vizzini USB Serial - https://github.com/shenki/exar-uart-driver
    # NET "UartRx" LOC = "A16"; # Bank = 0, Pin name = IO_L66N_SCP0, Sch name = USBB-RXD
    # NET "UartTx" LOC = "B16"; # Bank = 0, Pin name = IO_L66P_SCP1, Sch name = USBB-TXD
    ("serial", 0,
        Subsignal("rx", Pins("AB8"), IOStandard("LVCMOS33")),
        Subsignal("tx", Pins("AB9"), IOStandard("LVCMOS33")),
    ),

#        ("fpga_cfg",
#            Subsignal("din", Pins("T14")),
#            Subsignal("cclk", Pins("R14")),
#            Subsignal("init_b", Pins("T12")),
#            Subsignal("prog_b", Pins("A2")),
#            Subsignal("done", Pins("T15")),
#        ),
#        ("jtag",
#            Subsignal("tms", Pins("B2")),
#            Subsignal("tdo", Pins("B16")),
#            Subsignal("tdi", Pins("B1")),
#            Subsignal("tck", Pins("A15")),
#        ),

]

# This Micro-D HDMI connector only works when VCCB2 is set to 3V3.
_io_vccb2_3v3 = [
    ## PMOD Connector
    # Micro-D connector, marked as JB, on the same side as switches + LEDs
    # but on the underside of the board below MOD connector. Works as
    # either output or input because it isn't buffered. Also often referred
    # to as "JA".
    # JP12 connects VCC to 3.3V or 2.5V, make sure 3.3V is selected.
    # JP3 connects / disconnects 5V to HDMI pin 19.
    #  * To use as output, remove the jumper.
    #  * To use as input, make sure it is connected.
    # NET "JB<5>"  LOC = "T9"; # Bank = 2,  Pin name = IO_L32P_GCLK29, Sch name = JA-CLK_P
    # NET "JB<4>"  LOC = "V9"; # Bank = 2,  Pin name = IO_L32N_GCLK28, Sch name = JA-CLK_N
    # NET "JB<1>"  LOC = "R3"; # Bank = 2,  Pin name = IO_L62P_D5,     Sch name = JA-D0_P
    # NET "JB<0>"  LOC = "T3"; # Bank = 2,  Pin name = IO_L62N_D6,     Sch name = JA-D0_N
    # NET "JB<7>"  LOC = "T4"; # Bank = 2,  Pin name = IO_L63P,        Sch name = JA-D1_P
    # NET "JB<6>"  LOC = "V4"; # Bank = 2,  Pin name = IO_L63N,        Sch name = JA-D1_N
    # NET "JB<3>"  LOC = "N5"; # Bank = 2,  Pin name = IO_L64P_D8,     Sch name = JA-D2_P
    # NET "JB<2>"  LOC = "P6"; # Bank = 2,  Pin name = IO_L64N_D9,     Sch name = JA-D2_N
    ("hdmi_out", 1,
        Subsignal("clk_p", Pins("T9"), IOStandard("TMDS_33")),
        Subsignal("clk_n", Pins("V9"), IOStandard("TMDS_33")),
        Subsignal("data0_p", Pins("R3"), IOStandard("TMDS_33")),
        Subsignal("data0_n", Pins("T3"), IOStandard("TMDS_33")),
        Subsignal("data1_p", Pins("T4"), IOStandard("TMDS_33")),
        Subsignal("data1_n", Pins("V4"), IOStandard("TMDS_33")),
        Subsignal("data2_p", Pins("N5"), IOStandard("TMDS_33")),
        Subsignal("data2_n", Pins("P6"), IOStandard("TMDS_33")),
        # Make sure JP2 is connected. Shared with JA.
        #Subsignal("scl", Pins("C13"), IOStandard("LVCMOS33")),
        #Subsignal("sda", Pins("A13"), IOStandard("LVCMOS33")),
    ),
]

_io_vccb2_2v5 = []

_connectors = [
    ## onboard VHDCI - FIXME
    # Can either run at 2.5V or 3.3V dependent on JP12 connector.
    # Channel 1 connects to P signals, Channel 2 to N signals
    # NET "VHDCIIO1<0>"  LOC = "U16"; # Bank = 2,  Pin name = IO_L2P_CMPCLK,      Sch name = EXP-IO1_P
    # NET "VHDCIIO1<1>"  LOC = "U15"; # Bank = 2,  Pin name = *IO_L5P,            Sch name = EXP-IO2_P
    # NET "VHDCIIO1<2>"  LOC = "U13"; # Bank = 2,  Pin name = IO_L14P_D11,        Sch name = EXP-IO3_P
    # NET "VHDCIIO1<3>"  LOC = "M11"; # Bank = 2,  Pin name = *IO_L15P,           Sch name = EXP-IO4_P
    # NET "VHDCIIO1<4>"  LOC = "R11"; # Bank = 2,  Pin name = IO_L16P,            Sch name = EXP-IO5_P
    # NET "VHDCIIO1<5>"  LOC = "T12"; # Bank = 2,  Pin name = *IO_L19P,           Sch name = EXP-IO6_P
    # NET "VHDCIIO1<6>"  LOC = "N10"; # Bank = 2,  Pin name = *IO_L20P,           Sch name = EXP-IO7_P
    # NET "VHDCIIO1<7>"  LOC = "M10"; # Bank = 2,  Pin name = *IO_L22P,           Sch name = EXP-IO8_P
    # NET "VHDCIIO1<8>"  LOC = "U11"; # Bank = 2,  Pin name = IO_L23P,            Sch name = EXP-IO9_P
    # NET "VHDCIIO1<9>"  LOC = "R10"; # Bank = 2,  Pin name = IO_L29P_GCLK3,      Sch name = EXP-IO10_P
    # NET "VHDCIIO1<10>" LOC = "U10"; # Bank = 2,  Pin name = IO_L30P_GCLK1_D13,  Sch name = EXP-IO11_P
    # NET "VHDCIIO1<11>" LOC = "R8";  # Bank = 2,  Pin name = IO_L31P_GCLK31_D14, Sch name = EXP-IO12_P
    # NET "VHDCIIO1<12>" LOC = "M8";  # Bank = 2,  Pin name = *IO_L40P,           Sch name = EXP-IO13_P
    # NET "VHDCIIO1<13>" LOC = "U8";  # Bank = 2,  Pin name = IO_L41P,            Sch name = EXP-IO14_P
    # NET "VHDCIIO1<14>" LOC = "U7";  # Bank = 2,  Pin name = IO_L43P,            Sch name = EXP-IO15_P
    # NET "VHDCIIO1<15>" LOC = "N7";  # Bank = 2,  Pin name = *IO_L44P,           Sch name = EXP-IO16_P
    # NET "VHDCIIO1<16>" LOC = "T6";  # Bank = 2,  Pin name = IO_L45P,            Sch name = EXP-IO17_P
    # NET "VHDCIIO1<17>" LOC = "R7";  # Bank = 2,  Pin name = IO_L46P,            Sch name = EXP-IO18_P
    # NET "VHDCIIO1<18>" LOC = "N6";  # Bank = 2,  Pin name = *IO_L47P,           Sch name = EXP-IO19_P
    # NET "VHDCIIO1<19>" LOC = "U5";  # Bank = 2,  Pin name = IO_49P_D3,          Sch name = EXP-IO20_P
    # --
    # NET "VHDCIIO2<0>"  LOC = "V16"; # Bank = 2,  Pin name = IO_L2N_CMPMOSI,     Sch name = EXP-IO1_N
    # NET "VHDCIIO2<1>"  LOC = "V15"; # Bank = 2,  Pin name = *IO_L5N,            Sch name = EXP-IO2_N
    # NET "VHDCIIO2<2>"  LOC = "V13"; # Bank = 2,  Pin name = IO_L14N_D12,        Sch name = EXP-IO3_N
    # NET "VHDCIIO2<3>"  LOC = "N11"; # Bank = 2,  Pin name = *IO_L15N,           Sch name = EXP-IO4_N
    # NET "VHDCIIO2<4>"  LOC = "T11"; # Bank = 2,  Pin name = IO_L16N_VREF,       Sch name = EXP-IO5_N
    # NET "VHDCIIO2<5>"  LOC = "V12"; # Bank = 2,  Pin name = *IO_L19N,           Sch name = EXP-IO6_N
    # NET "VHDCIIO2<6>"  LOC = "P11"; # Bank = 2,  Pin name = *IO_L20N,           Sch name = EXP-IO7_N
    # NET "VHDCIIO2<7>"  LOC = "N9";  # Bank = 2,  Pin name = *IO_L22N,           Sch name = EXP-IO8_N
    # NET "VHDCIIO2<8>"  LOC = "V11"; # Bank = 2,  Pin name = IO_L23N,            Sch name = EXP-IO9_N
    # NET "VHDCIIO2<9>"  LOC = "T10"; # Bank = 2,  Pin name = IO_L29N_GCLK2,      Sch name = EXP-IO10_N
    # NET "VHDCIIO2<10>" LOC = "V10"; # Bank = 2,  Pin name = IO_L30N_GCLK0_USERCCLK, Sch name = EXP-IO11_N
    # NET "VHDCIIO2<11>" LOC = "T8";  # Bank = 2,  Pin name = IO_L31N_GCLK30_D15, Sch name = EXP-IO12_N
    # NET "VHDCIIO2<12>" LOC = "N8";  # Bank = 2,  Pin name = *IO_L40N,           Sch name = EXP-IO13_N
    # NET "VHDCIIO2<13>" LOC = "V8";  # Bank = 2,  Pin name = IO_L41N_VREF,       Sch name = EXP-IO14_N
    # NET "VHDCIIO2<14>" LOC = "V7";  # Bank = 2,  Pin name = IO_L43N,            Sch name = EXP-IO15_N
    # NET "VHDCIIO2<15>" LOC = "P8";  # Bank = 2,  Pin name = *IO_L44N,           Sch name = EXP-IO16_N
    # NET "VHDCIIO2<16>" LOC = "V6";  # Bank = 2,  Pin name = IO_L45N,            Sch name = EXP-IO17_N
    # NET "VHDCIIO2<17>" LOC = "T7";  # Bank = 2,  Pin name = IO_L46N,            Sch name = EXP-IO18_N
    # NET "VHDCIIO2<18>" LOC = "P7";  # Bank = 2,  Pin name = *IO_L47N,           Sch name = EXP-IO19_N
    # NET "VHDCIIO2<19>" LOC = "V5";  # Bank = 2,  Pin name = IO_49N_D4,          Sch name = EXP-IO20_N
    ("VHDCI",
        {
        "EXP-IO1_P": "U16",
        "EXP-IO2_P": "U15",
        "EXP-IO3_P": "U13",
        "EXP-IO4_P": "M11",
        "EXP-IO5_P": "R11",
        "EXP-IO6_P": "T12",
        "EXP-IO7_P": "N10",
        "EXP-IO8_P": "M10",
        "EXP-IO9_P": "U11",
        "EXP-IO10_P": "R10",
        "EXP-IO11_P": "U10",
        "EXP-IO12_P": "R8",
        "EXP-IO13_P": "M8",
        "EXP-IO14_P": "U8",
        "EXP-IO15_P": "U7",
        "EXP-IO16_P": "N7",
        "EXP-IO17_P": "T6",
        "EXP-IO18_P": "R7",
        "EXP-IO19_P": "N6",
        "EXP-IO20_P": "U5",
        "EXP-IO1_N": "V16",
        "EXP-IO2_N": "V15",
        "EXP-IO3_N": "V13",
        "EXP-IO4_N": "N11",
        "EXP-IO5_N": "T11",
        "EXP-IO6_N": "V12",
        "EXP-IO7_N": "P11",
        "EXP-IO8_N": "N9",
        "EXP-IO9_N": "V11",
        "EXP-IO10_N": "T10",
        "EXP-IO11_N": "V10",
        "EXP-IO12_N": "T8",
        "EXP-IO13_N": "N8",
        "EXP-IO14_N": "V8",
        "EXP-IO15_N": "V7",
        "EXP-IO16_N": "P8",
        "EXP-IO17_N": "V6",
        "EXP-IO18_N": "T7",
        "EXP-IO19_N": "P7",
        "EXP-IO20_N": "V5",
        }
    ),
]


_hdmi_infos = {
    "HDMI_IN0_MNEMONIC": "J1",
    "HDMI_IN0_DESCRIPTION" : (
      "  Type A connector, marked as J1, on side with USB connectors.\\r\\n"
      "  To use J1, make sure:\\r\\n"
      "   * JP4 has a jumper (it connects / disconnects 5V to HDMI pin 18).\\r\\n"
      "   * JP2 (marked only as SDA/SCL - not to be confused with JP6 and JP6)\\r\\n"
      "     has *two* jumpers (horizontally).\\r\\n"
      "   * JP5 has a jumper (it enables the HDMI input buffer).\\r\\n"
    ),

    "HDMI_IN1_MNEMONIC": "J3",
    "HDMI_IN1_DESCRIPTION" : (
      "  Type A connector, marked as J3, between audio connectors and\\r\\n"
      "  Ethernet RJ45 connector.\\r\\n"
      "  To use J3, make sure:\\r\\n"
      "  * JP8 has a jumper (it connects / disconnects 5V to HDMI pin 18)\\r\\n"
      "  * JP6 and JP7 do *not* have any jumpers (it connect J3's and J2's\\r\\n"
      "    EDID lines together).\\r\\n"
    ),

    "HDMI_OUT0_MNEMONIC": "J2",
    "HDMI_OUT0_DESCRIPTION" : (
      "  Type A connector, marked as J2, next to the power connector.\\r\\n"
      "  To use J2, make sure:\\r\\n"
      "  * JP8 has a jumper (it connects / disconnects 5V to HDMI pin 18)\\r\\n"
      "  * JP6 and JP7 do *not* have any jumpers (it connect J3's and J2's\\r\\n"
      "    EDID lines together).\\r\\n"
    ),

    "HDMI_OUT1_MNEMONIC": "JB",
    "HDMI_OUT1_DESCRIPTION" : (
      "  Micro-D connector, marked as JB, on the same side as switches\\r\\n"
      "  + LEDs but on the underside of the board below MOD connector.\\r\\n"
      "  Works as either output or input because it isn't buffered.\\r\\n"
      "  Also often referred to as 'JA'.\\r\\n"
    )
}


class Platform(XilinxPlatform):
    name = "amiro_image_processing"
    default_clk_name = "clk100"
    default_clk_period = 10.0
    hdmi_infos = _hdmi_infos

    # https://reference.digilentinc.com/atlys:atlys:refmanual#flash_memory
    # The Atlys has a XC6SLX45 which bitstream takes up ~12Mbit (1484472 bytes)
    # 0x200000 offset (16Mbit) gives plenty of space
    gateware_size = 0x200000

    # Micron N25Q128 (ID 0x0018ba20)
    # FIXME: Create a "spi flash module" object in the same way we have SDRAM
    # module objects.
    spiflash_model = "n25q128"
    spiflash_read_dummy_bits = 10
    spiflash_clock_div = 4
    spiflash_total_size = int((128/8)*1024*1024) # 128Mbit
    spiflash_page_size = 256
    spiflash_sector_size = 0x10000

    def __init__(self, programmer="openocd", vccb2_voltage="VCC3V3"):
        # Some IO configurations only work at certain vccb2 voltages.
       
        # XC6SLX45-2CSG324C
        XilinxPlatform.__init__(self,  "xc6slx100fgg484-2", _io, _connectors)
       

    def create_programmer(self):
	# Preferred programmer - Needs ixo-usb-jtag and latest openocd.
        proxy="bscan_spi_{}.bit".format(self.device.split('-')[0])
        if self.programmer == "openocd":
            return OpenOCD(config="board/digilent_atlys.cfg", flash_proxy_basename=proxy)
	# Alternative programmers - not regularly tested.
        elif self.programmer == "xc3sprog":
            return XC3SProg("jtaghs1_fast", "bscan_spi_digilent_atlys.bit")
        elif self.programmer == "impact":
            return iMPACT()
        elif self.programmer == "adept":
            return Adept("Atlys", 0)
        elif self.programmer == "fpgalink":
            from mibuild.fpgalink_programmer import FPGALink
            return FPGALink("1443:0007")
        elif self.programmer == "urjtag":
            return UrJTAG(cable="USBBlaster", pld="spartan-6")
        else:
            raise ValueError("{} programmer is not supported".format(self.programmer))

    def do_finalize(self, fragment):
        XilinxPlatform.do_finalize(self, fragment)

        # The oscillator clock sources.
        try:
            self.add_period_constraint(self.lookup_request("clk100", loose=True), 10.0)
        except ConstraintError:
            pass

        # HDMI input clock pins.
        for i in range(2):
            try:
                self.add_period_constraint(self.lookup_request("hdmi_in", i).clk_p, 12)
            except ConstraintError:
                pass

        # Ethernet input clock pins.
        try:
            self.add_period_constraint(self.lookup_request("eth_clocks").rx, 40.0)
        except ConstraintError:
            pass

        # USB input clock pins.
        try:
            self.add_period_constraint(self.lookup_request("fx2").ifclk, 10)
        except ConstraintError:
            pass



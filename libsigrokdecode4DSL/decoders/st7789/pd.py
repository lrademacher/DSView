import sigrokdecode as srd

COMMAND_MAP = {
    0x00: {"name": "NOP", "desc": "Empty command",},
    0x01: {"name": "SWRESET", "desc": "Software Reset",},
    0x04: {"name": "RDDID", "desc": "Read Display ID",},
    0x09: {"name": "RDDST", "desc": "Read Display Status",},
    0x0A: {"name": "RDDPM", "desc": "Read Display Power Mode",},
    0x0B: {"name": "RDDMADCTL", "desc": "Read Display MADCTL",},
    0x0C: {"name": "RDDCOLMOD", "desc": "Read Display Pixel Format",},
    0x0D: {"name": "RDDIM", "desc": "Read Display Image Mode",},
    0x0E: {"name": "RDDSM", "desc": "Read Display Signal Mode",},
    0x0F: {"name": "RDDSDR", "desc": "Read Display Self-Diagnostic Result",},
    0x10: {"name": "SLPIN", "desc": "Sleep in",},
    0x11: {"name": "SLPOUT", "desc": "Sleep Out",},
    0x12: {"name": "PTLON", "desc": "Partial Display Mode On",},
    0x13: {"name": "NORON", "desc": "Normal Display Mode On",},
    0x20: {"name": "INVOFF", "desc": "Display Inversion Off",},
    0x21: {"name": "INVON", "desc": "Display Inversion On",},
    0x26: {"name": "GAMSET", "desc": "Gamma Set",},
    0x28: {"name": "DISPOFF", "desc": "Display Off",},
    0x29: {"name": "DISPON", "desc": "Display On",},
    0x2A: {"name": "CASET", "desc": "Column Address Set",},
    0x2B: {"name": "RASET", "desc": "Row Address Set",},
    0x2C: {"name": "RAMWR", "desc": "Memory Write",},
    0x2E: {"name": "RAMRD", "desc": "Memory Read",},
    0x30: {"name": "PTLAR", "desc": "Partial Area",},
    0x33: {"name": "VSCRDEF", "desc": "Vertical Scrolling Definition",},
    0x34: {"name": "TEOFF", "desc": "Tearing Effect Line OFF",},
    0x35: {"name": "TEON", "desc": "Tearing Effect Line On",},
    0x36: {"name": "MADCTL", "desc": "Memory Data Access Control",},
    0x37: {"name": "VSCSAD", "desc": "Vertical Scroll Start Address of RAM",},
    0x38: {"name": "IDMOFF", "desc": "Idle Mode Off",},
    0x39: {"name": "IDMON", "desc": "Idle mode on",},
    0x3A: {"name": "COLMOD", "desc": "Interface Pixel Format",},
    0x3C: {"name": "WRMEMC", "desc": "Write Memory Continue",},
    0x3E: {"name": "RDMEMC", "desc": "Read Memory Continue",},
    0x44: {"name": "STE", "desc": "Set Tear Scanline",},
    0x45: {"name": "GSCAN", "desc": "Get Scanline",},
    0x51: {"name": "WRDISBV", "desc": "Write Display Brightness",},
    0x52: {"name": "RDDISBV", "desc": "Read Display Brightness Value",},
    0x53: {"name": "WRCTRLD", "desc": "Write CTRL Display",},
    0x54: {"name": "RDCTRLD", "desc": "Read CTRL Value Display",},
    0x55: {
        "name": "WRCACE",
        "desc": "Write Content Adaptive Brightness Control and Color Enhancement",
    },
    0x56: {"name": "RDCABC", "desc": "Read Content Adaptive Brightness Control",},
    0x5E: {"name": "WRCABCMB", "desc": "Write CABC Minimum Brightness",},
    0x5F: {"name": "RDCABCMB", "desc": "Read CABC Minimum Brightness",},
    0x68: {
        "name": "RDABCSDR",
        "desc": "Read Automatic Brightness Control Self-Diagnostic Result",
    },
    0xDA: {"name": "RDID1", "desc": "Read ID1",},
    0xDB: {"name": "RDID2", "desc": "Read ID2",},
    0xDC: {"name": "RDID3", "desc": "Read ID3",},
    0xB0: {"name": "RAMCTRL", "desc": "RAM Control",},
    0xB1: {"name": "RGBCTRL", "desc": "RGB Interface Control",},
    0xB2: {"name": "PORCTRL", "desc": "Porch Setting",},
    0xB3: {
        "name": "FRCTRL1",
        "desc": "Frame Rate Control 1 (In partial mode/ idle colors)",
    },
    0xB5: {"name": "PARCTRL", "desc": "Partial mode Control",},
    0xB7: {"name": "GCTRL", "desc": "Gate Control",},
    0xB8: {"name": "GTADJ", "desc": "Gate On Timing Adjustment",},
    0xBA: {"name": "DGMEN", "desc": "Digital Gamma Enable",},
    0xBB: {"name": "VCOMS", "desc": "VCOMS Setting",},
    0xC0: {"name": "LCMCTRL", "desc": "LCM Control",},
    0xC1: {"name": "IDSET", "desc": "ID Code Setting",},
    0xC2: {"name": "VDVVRHEN", "desc": "VDV and VRH Command Enable",},
    0xC3: {"name": "VRHS", "desc": "VRH Set",},
    0xC4: {"name": "VDVS", "desc": "VDV Set",},
    0xC5: {"name": "VCMOFSET", "desc": "VCOMS Offset Set",},
    0xC6: {"name": "FRCTRL2", "desc": "Frame Rate Control in Normal Mode",},
    0xC7: {"name": "CABCCTRL", "desc": "CABC Control",},
    0xC8: {"name": "REGSEL1", "desc": "Register Value Selection 1",},
    0xCA: {"name": "REGSEL2", "desc": "Register Value Selection 2",},
    0xCC: {"name": "PWMFRSEL", "desc": "PWM Frequency Selection",},
    0xD0: {"name": "PWCTRL1", "desc": "Power Control 1",},
    0xD2: {"name": "VAPVANEN", "desc": "Enable VAP/VAN signal output",},
    0xDF: {"name": "CMD2EN", "desc": "Command 2 Enable",},
    0xE0: {"name": "PVGAMCTRL", "desc": "Positive Voltage Gamma Control",},
    0xE1: {"name": "NVGAMCTRL", "desc": "Negative Voltage Gamma Control",},
    0xE2: {"name": "DGMLUTR", "desc": "Digital Gamma Look-up Table for Red",},
    0xE3: {"name": "DGMLUTB", "desc": "Digital Gamma Look-up Table for Blue",},
    0xE4: {"name": "GATECTRL", "desc": "Gate Control",},
    0xE7: {"name": "SPI2EN", "desc": "SPI2 Enable",},
    0xE8: {"name": "PWCTRL2", "desc": "Power Control 2",},
    0xE9: {"name": "EQCTRL", "desc": "Equalize time control",},
    0xEC: {"name": "PROMCTRL", "desc": "Program Mode Control",},
    0xFA: {"name": "PROMEN", "desc": "Program Mode Enable",},
    0xFC: {"name": "NVMSET", "desc": "NVM Setting",},
    0xFE: {"name": "PROMACT", "desc": "Program action",},
}


class Chn:
    CS, CLK, MOSI, DC = range(4)


class Ann:
    BITS, CMD, DATA, CMD_DATA, ASRT = range(5)


class Decoder(srd.Decoder):
    api_version = 3
    id = "st7789"
    name = "ST7789"
    longname = "Sitronix ST7789"
    desc = "Sitronix ST7789 TFT controller protocol."
    license = "gplv2+"
    inputs = ["logic"]
    outputs = []
    channels = (
        {"id": "cs", "name": "CS#", "desc": "Chip-select"},
        {"id": "clk", "name": "CLK", "desc": "Clock"},
        {"id": "mosi", "name": "MOSI", "desc": "Master out, slave in"},
        {"id": "dc", "name": "DC", "desc": "Data or command"},
    )
    optional_channels = tuple()
    tags = ["Display", "SPI"]
    annotations = (
        ("bit", "Bit"),
        ("command", "Command"),
        ("data", "Data"),
        ("cmd_data", "Command + Data"),
        ("asserted", "Assertion"),
    )
    annotation_rows = (
        ("bits", "Bits", (Ann.BITS,)),
        ("bytes", "Bytes", (Ann.CMD, Ann.DATA,)),
        ("cmd_data", "Command + Data", (Ann.CMD_DATA,)),
        ("asserted", "Assertion", (Ann.ASRT,)),
    )

    def __init__(self):
        self.reset()

    def reset(self):
        pass

    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)

    def _get_cmd_str(self, cmd):
        if cmd in COMMAND_MAP:
            return COMMAND_MAP[cmd]["name"] + "(%02X)" % cmd
        else:
            return "Unknown(%02X)" % cmd

    def _get_cmd_data_str(self, cmd, data_list):
        cmd_str = self._get_cmd_str(cmd)

        if data_list:
            ret_str = f"{cmd_str}: "
            for v in data_list:
                ret_str += " %02X" % v
            return ret_str
        else:
            return cmd_str

    def decode(self):
        last_cmd = None
        last_cmd_data_sample_startnum = None
        last_cmd_data_sample_endnum = None
        last_cmd_data_list = []

        while True:
            self.wait({Chn.CS: "f"})
            cs_start_samplenum = self.samplenum

            bit = None
            bit_count = 0
            byte = 0
            byte_sample_startnum = None

            while True:
                (cs, clk, mosi, dc) = self.wait([{Chn.CS: "r"}, {Chn.CLK: "r"}])
                if cs == 1:
                    self.put(
                        cs_start_samplenum,
                        self.samplenum,
                        self.out_ann,
                        [Ann.ASRT, ["Asserted"]],
                    )

                    if last_cmd is not None:
                        self.put(
                            last_cmd_data_sample_startnum,
                            last_cmd_data_sample_endnum,
                            self.out_ann,
                            [
                                Ann.CMD_DATA,
                                [self._get_cmd_data_str(last_cmd, last_cmd_data_list)],
                            ],
                        )
                        last_cmd = None
                        last_cmd_data_sample_startnum = None
                        last_cmd_data_sample_endnum = None
                        last_cmd_data_list = []

                    break

                if clk == 1 and bit is None:
                    bit = mosi
                    bit_start_samplenum = self.samplenum
                    bit_count += 1
                    byte = (byte << 1) | bit
                    if byte_sample_startnum is None:
                        byte_sample_startnum = self.samplenum

                if clk == 0 and bit is not None:
                    self.put(
                        bit_start_samplenum,
                        self.samplenum,
                        self.out_ann,
                        [Ann.BITS, [str(bit)]],
                    )
                    bit = None
                    if bit_count == 8:
                        if dc:
                            last_cmd_data_sample_endnum = self.samplenum
                            last_cmd_data_list.append(byte)
                            self.put(
                                byte_sample_startnum,
                                self.samplenum,
                                self.out_ann,
                                [Ann.DATA, ["Data(%02X)" % byte]],
                            )
                        else:
                            self.put(
                                byte_sample_startnum,
                                self.samplenum,
                                self.out_ann,
                                [Ann.CMD, [self._get_cmd_str(byte)]],
                            )

                            if last_cmd is not None:
                                self.put(
                                    last_cmd_data_sample_startnum,
                                    last_cmd_data_sample_endnum,
                                    self.out_ann,
                                    [
                                        Ann.CMD_DATA,
                                        [
                                            self._get_cmd_data_str(
                                                last_cmd, last_cmd_data_list
                                            )
                                        ],
                                    ],
                                )
                                last_cmd_data_list = []

                            last_cmd = byte
                            last_cmd_data_sample_startnum = byte_sample_startnum
                            last_cmd_data_sample_endnum = self.samplenum

                        byte = 0
                        bit_count = 0
                        byte_sample_startnum = None

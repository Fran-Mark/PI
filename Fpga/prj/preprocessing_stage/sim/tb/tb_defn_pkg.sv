package tb_defn_pkg;

  // TB Top definitions.
  localparam int RESET_CLOCK_COUNT = 50;
  localparam int ADC_CLK_FREQ_HZ = 260e6;
  localparam realtime ADC_CLK_PERIOD = 1s / ADC_CLK_FREQ_HZ;

  localparam int AXI_CLK_FREQ_HZ = 100e6;
  localparam time AXI_CLK_PERIOD = 1s / AXI_CLK_FREQ_HZ;

  localparam logic[15:0] OFFSET_ADDR = 16'h0000;
  localparam logic[4:0] SEL_SOURCE_ADDR = 5'b00000;
  localparam int DATA_WIDTH=32;
  localparam int ADDR_WIDTH=4;
  localparam int WSTRB_WIDTH = DATA_WIDTH / 8;
  localparam logic[WSTRB_WIDTH-1:0] WSTRB_AGREGADO = 4'b1111;

  localparam real FREQ_TONO_MHZ = 19.51;
  localparam real FREQ_TONO_MHZ_2 = 19.42;
  localparam real FREQ_TONO_MHZ_3 = 16.7;
  localparam real FREQ_LOW_MHZ = 2;
  localparam real PI_CONST = 3.14159265;
  localparam int LARGO_TONO = 50000;

  localparam int SIM_PKT_NUM = 10;

  localparam int ADC_WIDTH = 14;

  localparam int CLOCKS_PER_SAMPLE = 3;

  localparam real NOISE_LEVEL = 0.8;

endpackage : tb_defn_pkg
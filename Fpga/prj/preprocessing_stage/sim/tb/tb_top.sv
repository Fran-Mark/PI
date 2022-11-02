`timescale 1ps/1ps
module tb_top;

  // Imports.
  import uvm_pkg::*;
  import tb_defn_pkg::*;
  import tb_test_pkg::*;


  `include "uvm_macros.svh"

  // Clock and reset signals.
  logic axi_clk;
  logic adc_clk;
  logic rst_n;
  logic aux_rst_n;
  logic [13:0] data;
  logic valid;

  stream_if #(
      .DATA_WIDTH(14)
  ) stream_if_inst (
      .rst_n(aux_rst_n),
      .clk  (adc_clk)
  );
  assign stream_if_inst.ready = 1'b1;


  stream_ADDR1_if awaddr_if (
      .clk  (axi_clk),
      .rst_n(aux_rst_n)
  );

  stream_if #(
      .DATA_WIDTH(DATA_WIDTH + WSTRB_WIDTH)
  ) wdata_if (
      .clk  (axi_clk),
      .rst_n(aux_rst_n)
  );

  stream_slave_if #(
      .DATA_WIDTH(2)
  ) bresp_if (
      .clk  (axi_clk),
      .rst_n(aux_rst_n)
  );


 stream_ADDR2_if  araddr_if (
      .clk  (axi_clk),
      .rst_n(aux_rst_n)
  );


  stream_slave_if #(
      .DATA_WIDTH(DATA_WIDTH + 2)
  ) rresp_if (
      .clk  (axi_clk),
      .rst_n(aux_rst_n)
  );



  always_comb begin
    data <= stream_if_inst.data;
    valid <= stream_if_inst.valid;
  end

  //DUT
preprocessing_bd_wrapper preprocessing_bd_wrapper_i(
    .adc_clk(adc_clk),
    .adc_rst_ni(aux_rst_n),
    .adc_tvalid_0(valid),
    .data_in_0(data),
    .AXI_CLK(axi_clk),
    .AXI_ARESETN(rst_n),

    .S00_AXI_0_araddr (araddr_if.data[ADDR_WIDTH-1:0]),
    .S00_AXI_0_arprot (3'b0),
    .S00_AXI_0_arready(araddr_if.ready),
    .S00_AXI_0_arvalid(araddr_if.valid),
    .S00_AXI_0_awaddr (awaddr_if.data[ADDR_WIDTH-1:0]),
    .S00_AXI_0_awprot (3'b0),
    .S00_AXI_0_awready (awaddr_if.ready),
    .S00_AXI_0_awvalid (awaddr_if.valid),
    .S00_AXI_0_bready (bresp_if.ready),
    .S00_AXI_0_bresp (bresp_if.data[1:0]),
    .S00_AXI_0_bvalid (bresp_if.valid),
    .S00_AXI_0_rdata (rresp_if.data[DATA_WIDTH-1:0]),
    .S00_AXI_0_rready (rresp_if.ready),
    .S00_AXI_0_rresp (rresp_if.data[DATA_WIDTH + 1:DATA_WIDTH ]),
    .S00_AXI_0_rvalid (rresp_if.valid),
    .S00_AXI_0_wdata (wdata_if.data[DATA_WIDTH+WSTRB_WIDTH-1:WSTRB_WIDTH]),
    .S00_AXI_0_wready (wdata_if.ready),
    .S00_AXI_0_wstrb (wdata_if.data[WSTRB_WIDTH-1:0]),
    .S00_AXI_0_wvalid (wdata_if.valid)

);

  // Clock and reset initial block.
  // Clock and reset initial block.
  initial begin

    fork
        begin
            // Initialize clock to 0 and reset_n to TRUE.
            adc_clk   = 0;
            rst_n = 0;
            aux_rst_n = 0;
            //#(ADC_CLK_PERIOD/2) adc_clk <= ~adc_clk;
            // Wait for reset completion (RESET_CLOCK_COUNT).
            repeat (RESET_CLOCK_COUNT) begin
            #(ADC_CLK_PERIOD / 2) adc_clk = 0;
            #(ADC_CLK_PERIOD - ADC_CLK_PERIOD / 2) adc_clk = 1;
            end

            aux_rst_n = 1;

            repeat (RESET_CLOCK_COUNT) begin
            #(ADC_CLK_PERIOD / 2) adc_clk = 0;
            #(ADC_CLK_PERIOD - ADC_CLK_PERIOD / 2) adc_clk = 1;
            end
            // Set rst to FALSE.
            rst_n = 1;
            forever begin
            #(ADC_CLK_PERIOD / 2) adc_clk = 0;
            #(ADC_CLK_PERIOD - ADC_CLK_PERIOD / 2) adc_clk = 1;
            end
        end

        begin
            // Initialize clock to 0 and reset_n to TRUE.
            axi_clk   = 0;
            forever begin
            #(AXI_CLK_PERIOD / 2) axi_clk = 0;
            #(AXI_CLK_PERIOD - AXI_CLK_PERIOD / 2) axi_clk = 1;
            end
        end
    join
  end


  initial begin
    // Set default verbosity level for all TB components.
    uvm_top.set_report_verbosity_level(UVM_HIGH);
    // Set time format for simulation.
    $timeformat(-12, 1, " ps", 1);

    // Configure some simulation options.
    uvm_top.enable_print_topology = 1;
    uvm_top.finish_on_completion  = 0;
    // Register concrete classes
    stream_if_inst.register_interface("stream_if");
    // Register concrete classes
    awaddr_if.register_interface("awaddr_if");
    wdata_if.register_interface("wdata_if");
    bresp_if.register_interface("bresp_if");

    araddr_if.register_interface("araddr_if");
    rresp_if.register_interface("rresp_if");
    // Test name must be set from the simulator's command line.
    run_test();
    $stop();
  end



endmodule : tb_top

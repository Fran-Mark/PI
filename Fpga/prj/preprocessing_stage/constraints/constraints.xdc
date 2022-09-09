
create_clock -period 3.846 -name adc_clk [get_ports adc_clk]


create_clock -period 10.000 -name AXI_CLK [get_ports AXI_CLK]

set_false_path -from [get_pins {preprocessing_bd_i/AXI_hier/axi_slave_reg_0/U0/slv_reg0_reg*/C}] -to [get_pins {preprocessing_bd_i/cdc_hier/cdc_two_ff_sync_0/U0/reg_1_reg[0]/D}]

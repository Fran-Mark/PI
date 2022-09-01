set clock_frequency_mhz 260

create_clock -period [expr 1e3/$clock_frequency_mhz] \
    -name adc_clk [get_ports adc_clk]


create_clock -period [expr 1e3/100] \
    -name AXI_CLK [get_ports AXI_CLK]

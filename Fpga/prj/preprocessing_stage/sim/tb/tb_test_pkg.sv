//Package of the test class
package tb_test_pkg;

  // Package imports.
  import uvm_pkg::*;
  `include "uvm_macros.svh"

  import tb_defn_pkg::*;
  import tb_env_pkg::*;
  import tb_vseq_pkg::*;

  // Agent package imports.
  import stream_agent_pkg::*;

  import stream_ADDR1_agent_pkg::*;
  import stream_ADDR2_agent_pkg::*;
  import stream_slave_agent_pkg::*;


  //------------------------------------------------------------------------------
  // Class: tb_test_base
  //------------------------------------------------------------------------------
  // Verification test base for tb design.
  //------------------------------------------------------------------------------
  class tb_test_base extends uvm_test;
    // UVM Factory Registration Macro
    `uvm_component_utils(tb_test_base)

    // Environment class instantiation.
    tb_env m_env;
    // Environment configuration object instantiation.
    tb_env_config env_config;

    // Constructor.
    function new(string name, uvm_component parent);
      super.new(name, parent);
    endfunction : new

    // Test's build phase.
    function void build_phase(uvm_phase phase);
      // Must always call parent method's build phase.
      super.build_phase(phase);

      // Create environment and its configuration object.
      m_env = tb_env::type_id::create("m_env", this);
      env_config = tb_env_config::type_id::create("env_config");


      // Configure Stream eth_in Agent.
      env_config.m_stream_agent_config =
          stream_agent_config::type_id::create("m_stream_agent_config");
      env_config.m_stream_agent_config.active = UVM_ACTIVE;
      env_config.m_stream_agent_config.interface_name = "stream_if";


          // Configure Stream Agent.
      env_config.m_araddr_agent_config =
          stream_ADDR2_agent_config::type_id::create("m_araddr_agent_config");
      env_config.m_araddr_agent_config.active = UVM_ACTIVE;
      env_config.m_araddr_agent_config.interface_name = "araddr_if";


      // Configure Stream Slave Agent.
      env_config.m_rresp_agent_config =
          stream_slave_agent_config::type_id::create("m_rresp_agent_config");
      env_config.m_rresp_agent_config.active = UVM_ACTIVE;
      env_config.m_rresp_agent_config.interface_name = "rresp_if";


      // Configure Stream Agent.
      env_config.m_awaddr_agent_config =
          stream_ADDR1_agent_config::type_id::create("m_awaddr_agent_config");
      env_config.m_awaddr_agent_config.active = UVM_ACTIVE;
      env_config.m_awaddr_agent_config.interface_name = "awaddr_if";


      // Configure Stream Agent.
      env_config.m_wdata_agent_config =
          stream_agent_config::type_id::create("m_wdata_agent_config");
      env_config.m_wdata_agent_config.active = UVM_ACTIVE;
      env_config.m_wdata_agent_config.interface_name = "wdata_if";


      // Configure Stream Slave Agent.
      env_config.m_bresp_agent_config =
          stream_slave_agent_config::type_id::create("m_bresp_agent_config");
      env_config.m_bresp_agent_config.active = UVM_ACTIVE;
      env_config.m_bresp_agent_config.interface_name = "bresp_if";


      // Environment post configuration
      configure_env(env_config);

      // Post configure and set configuration object to database
      uvm_config_db#(tb_env_config)::set(this, "*", "tb_env_config", env_config);
    endfunction : build_phase

    // Convenience method used by test sub-classes to modify the environment.
    virtual function void configure_env(tb_env_config env_config);
      // Environment post config here (if needed).
    endfunction : configure_env

    function void init_adc_vseq(tb_vseq_base vseq);
      if (env_config.has_stream_agent) begin
        vseq.stream_sqr = m_env.m_stream_agent.m_sequencer;
      end
    endfunction : init_adc_vseq


    function void init_axi_vseq(tb_vseq_base seq);
          if (env_config.has_araddr_stream_if) begin
        seq.araddr_sqr = m_env.m_araddr_stream.m_sequencer;
      end

      if (env_config.has_rresp_if_stream_slave_if) begin
        seq.rresp_sqr = m_env.m_rresp_stream_slave.m_sequencer;
      end


      if(env_config.has_awaddr_stream_if) begin
        seq.awaddr_sqr = m_env.m_awaddr_stream.m_sequencer;
      end
      
      if(env_config.has_wdata_stream_if) begin
        seq.wdata_sqr = m_env.m_wdata_stream.m_sequencer;
      end

      if(env_config.has_bresp_if_stream_slave_if) begin
        seq.bresp_sqr = m_env.m_bresp_stream_slave.m_sequencer;
      end
      
    endfunction : init_axi_vseq


  endclass : tb_test_base


  //------------------------------------------------------------------------------
  // Class: tb_simple_stream_test
  //------------------------------------------------------------------------------

  class tb_simple_stream_test extends tb_test_base;
    // UVM Factory Registration Macro
    `uvm_component_utils(tb_simple_stream_test)

    // Constructor.
    function new(string name, uvm_component parent);
      super.new(name, parent);
    endfunction : new

    // Test's build phase.
    function void build_phase(uvm_phase phase);
      super.build_phase(phase);
    endfunction : build_phase

    // Environment configuration for current test.
    function void configure_env(tb_env_config env_config);
      env_config.has_stream_agent = 1'b1;
      //env_config.has_eth_stream_layering = 1'b1;

      env_config.has_araddr_stream_if = 1'b1;
      env_config.has_rresp_if_stream_slave_if = 1'b1;
      env_config.has_awaddr_stream_if = 1'b1;
      env_config.has_wdata_stream_if = 1'b1;
      env_config.has_bresp_if_stream_slave_if = 1'b1;

    endfunction : configure_env

    // // Main task executed by the test.
    task run_phase(uvm_phase phase);
      tb_vseq_stream_trasm eth_trasm_vseq;
      
      //Transmitimos un write al registro (un 1)
      tb_seq_write write_seq;

      //write_seq = tb_seq_write::type_id::create("write_seq");
      eth_trasm_vseq = tb_vseq_stream_trasm::type_id::create("eth_trasm_vseq");

       //init_axi_vseq(write_seq);

      init_adc_vseq(eth_trasm_vseq);


      uvm_test_done.raise_objection(this);

      //fork
        begin
          eth_trasm_vseq.start(null);
        end

      //   begin
      //     #(50us);
      //     $display("Escribiendo 1 en data source control");

      //     if (!write_seq.randomize() with {
      //           addr == SEL_SOURCE_ADDR + OFFSET_ADDR;
      //           data == 1;
      //         }) begin
      //       `uvm_error(get_full_name(), "Failed to randomize sequence!");
      //     end
      //     write_seq.start(null);
      //    end

      // join

      #(1ms);
      uvm_test_done.drop_objection(this);

    endtask : run_phase


  endclass : tb_simple_stream_test
  

endpackage : tb_test_pkg

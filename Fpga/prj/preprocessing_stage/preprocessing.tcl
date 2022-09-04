
################################################################
# This is a generated script based on design: preprocessing_bd
#
# Though there are limitations about the generated script,
# the main purpose of this utility is to make learning
# IP Integrator Tcl commands easier.
################################################################

namespace eval _tcl {
proc get_script_folder {} {
   set script_path [file normalize [info script]]
   set script_folder [file dirname $script_path]
   return $script_folder
}
}
variable script_folder
set script_folder [_tcl::get_script_folder]

################################################################
# Check if script is running in correct Vivado version.
################################################################
set scripts_vivado_version 2020.2
set current_vivado_version [version -short]

if { [string first $scripts_vivado_version $current_vivado_version] == -1 } {
   puts ""
   catch {common::send_gid_msg -ssname BD::TCL -id 2041 -severity "ERROR" "This script was generated using Vivado <$scripts_vivado_version> and is being run in <$current_vivado_version> of Vivado. Please run the script in Vivado <$scripts_vivado_version> then open the design in Vivado <$current_vivado_version>. Upgrade the design by running \"Tools => Report => Report IP Status...\", then run write_bd_tcl to create an updated script."}

   return 1
}

################################################################
# START
################################################################

# To test this script, run the following commands from Vivado Tcl console:
# source preprocessing_bd_script.tcl


# The design that will be created by this Tcl script contains the following 
# module references:
# axi_slave_reg, dsp_complex_gain, dsp_complex_gain, dsp_dds_compiler_controller, basic_counter, dsp_data_source_mux, valid_data_holder, zero_padder, zero_padder, dsp_dds_compiler_controller

# Please add the sources of those modules before sourcing this Tcl script.

# If there is no project opened, this script will create a
# project, but make sure you do not have an existing project
# <./myproj/project_1.xpr> in the current working folder.

set list_projs [get_projects -quiet]
if { $list_projs eq "" } {
   create_project project_1 myproj -part xc7z030fbg676-2
   set_property BOARD_PART www.proyecto-ciaa.com.ar:ciaa-acc:part0:1.0 [current_project]
}


# CHANGE DESIGN NAME HERE
variable design_name
set design_name preprocessing_bd

# If you do not already have an existing IP Integrator design open,
# you can create a design using the following command:
#    create_bd_design $design_name

# Creating design if needed
set errMsg ""
set nRet 0

set cur_design [current_bd_design -quiet]
set list_cells [get_bd_cells -quiet]

if { ${design_name} eq "" } {
   # USE CASES:
   #    1) Design_name not set

   set errMsg "Please set the variable <design_name> to a non-empty value."
   set nRet 1

} elseif { ${cur_design} ne "" && ${list_cells} eq "" } {
   # USE CASES:
   #    2): Current design opened AND is empty AND names same.
   #    3): Current design opened AND is empty AND names diff; design_name NOT in project.
   #    4): Current design opened AND is empty AND names diff; design_name exists in project.

   if { $cur_design ne $design_name } {
      common::send_gid_msg -ssname BD::TCL -id 2001 -severity "INFO" "Changing value of <design_name> from <$design_name> to <$cur_design> since current design is empty."
      set design_name [get_property NAME $cur_design]
   }
   common::send_gid_msg -ssname BD::TCL -id 2002 -severity "INFO" "Constructing design in IPI design <$cur_design>..."

} elseif { ${cur_design} ne "" && $list_cells ne "" && $cur_design eq $design_name } {
   # USE CASES:
   #    5) Current design opened AND has components AND same names.

   set errMsg "Design <$design_name> already exists in your project, please set the variable <design_name> to another value."
   set nRet 1
} elseif { [get_files -quiet ${design_name}.bd] ne "" } {
   # USE CASES: 
   #    6) Current opened design, has components, but diff names, design_name exists in project.
   #    7) No opened design, design_name exists in project.

   set errMsg "Design <$design_name> already exists in your project, please set the variable <design_name> to another value."
   set nRet 2

} else {
   # USE CASES:
   #    8) No opened design, design_name not in project.
   #    9) Current opened design, has components, but diff names, design_name not in project.

   common::send_gid_msg -ssname BD::TCL -id 2003 -severity "INFO" "Currently there is no design <$design_name> in project, so creating one..."

   create_bd_design $design_name

   common::send_gid_msg -ssname BD::TCL -id 2004 -severity "INFO" "Making design <$design_name> as current_bd_design."
   current_bd_design $design_name

}

common::send_gid_msg -ssname BD::TCL -id 2005 -severity "INFO" "Currently the variable <design_name> is equal to \"$design_name\"."

if { $nRet != 0 } {
   catch {common::send_gid_msg -ssname BD::TCL -id 2006 -severity "ERROR" $errMsg}
   return $nRet
}

set bCheckIPsPassed 1
##################################################################
# CHECK IPs
##################################################################
set bCheckIPs 1
if { $bCheckIPs == 1 } {
   set list_check_ips "\ 
xilinx.com:ip:cmpy:6.0\
xilinx.com:ip:dds_compiler:6.0\
xilinx.com:ip:fir_compiler:7.2\
"

   set list_ips_missing ""
   common::send_gid_msg -ssname BD::TCL -id 2011 -severity "INFO" "Checking if the following IPs exist in the project's IP catalog: $list_check_ips ."

   foreach ip_vlnv $list_check_ips {
      set ip_obj [get_ipdefs -all $ip_vlnv]
      if { $ip_obj eq "" } {
         lappend list_ips_missing $ip_vlnv
      }
   }

   if { $list_ips_missing ne "" } {
      catch {common::send_gid_msg -ssname BD::TCL -id 2012 -severity "ERROR" "The following IPs are not found in the IP Catalog:\n  $list_ips_missing\n\nResolution: Please add the repository containing the IP(s) to the project." }
      set bCheckIPsPassed 0
   }

}

##################################################################
# CHECK Modules
##################################################################
set bCheckModules 1
if { $bCheckModules == 1 } {
   set list_check_mods "\ 
axi_slave_reg\
dsp_complex_gain\
dsp_complex_gain\
dsp_dds_compiler_controller\
basic_counter\
dsp_data_source_mux\
valid_data_holder\
zero_padder\
zero_padder\
dsp_dds_compiler_controller\
"

   set list_mods_missing ""
   common::send_gid_msg -ssname BD::TCL -id 2020 -severity "INFO" "Checking if the following modules exist in the project's sources: $list_check_mods ."

   foreach mod_vlnv $list_check_mods {
      if { [can_resolve_reference $mod_vlnv] == 0 } {
         lappend list_mods_missing $mod_vlnv
      }
   }

   if { $list_mods_missing ne "" } {
      catch {common::send_gid_msg -ssname BD::TCL -id 2021 -severity "ERROR" "The following module(s) are not found in the project: $list_mods_missing" }
      common::send_gid_msg -ssname BD::TCL -id 2022 -severity "INFO" "Please add source files for the missing module(s) above."
      set bCheckIPsPassed 0
   }
}

if { $bCheckIPsPassed != 1 } {
  common::send_gid_msg -ssname BD::TCL -id 2023 -severity "WARNING" "Will not continue with creation of design due to the error(s) above."
  return 3
}

##################################################################
# DESIGN PROCs
##################################################################


# Hierarchical cell: Local_osc_hier
proc create_hier_cell_Local_osc_hier { parentCell nameHier } {

  variable script_folder

  if { $parentCell eq "" || $nameHier eq "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2092 -severity "ERROR" "create_hier_cell_Local_osc_hier() - Empty argument(s)!"}
     return
  }

  # Get object for parentCell
  set parentObj [get_bd_cells $parentCell]
  if { $parentObj == "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2090 -severity "ERROR" "Unable to find parent cell <$parentCell>!"}
     return
  }

  # Make sure parentObj is hier blk
  set parentType [get_property TYPE $parentObj]
  if { $parentType ne "hier" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2091 -severity "ERROR" "Parent <$parentObj> has TYPE = <$parentType>. Expected to be <hier>."}
     return
  }

  # Save current instance; Restore later
  set oldCurInst [current_bd_instance .]

  # Set parent object as current
  current_bd_instance $parentObj

  # Create cell and set as current instance
  set hier_obj [create_bd_cell -type hier $nameHier]
  current_bd_instance $hier_obj

  # Create interface pins

  # Create pins
  create_bd_pin -dir I -type clk adc_clk
  create_bd_pin -dir I adc_rst_ni
  create_bd_pin -dir O -from 15 -to 0 m_axis_tdata
  create_bd_pin -dir O m_axis_tvalid

  # Create instance: Local_oscillator, and set properties
  set Local_oscillator [ create_bd_cell -type ip -vlnv xilinx.com:ip:dds_compiler:6.0 Local_oscillator ]
  set_property -dict [ list \
   CONFIG.DATA_Has_TLAST {Not_Required} \
   CONFIG.DDS_Clock_Rate {260} \
   CONFIG.Frequency_Resolution {0.4} \
   CONFIG.Has_Phase_Out {false} \
   CONFIG.Has_TREADY {true} \
   CONFIG.Latency {9} \
   CONFIG.M_DATA_Has_TUSER {Not_Required} \
   CONFIG.Noise_Shaping {None} \
   CONFIG.Output_Frequency1 {0} \
   CONFIG.Output_Selection {Cosine} \
   CONFIG.Output_Width {16} \
   CONFIG.PINC1 {100101011010101} \
   CONFIG.Parameter_Entry {Hardware_Parameters} \
   CONFIG.Phase_Increment {Fixed} \
   CONFIG.Phase_Width {16} \
   CONFIG.S_PHASE_Has_TUSER {Not_Required} \
 ] $Local_oscillator

  # Create instance: dsp_dds_compiler_con_0, and set properties
  set block_name dsp_dds_compiler_controller
  set block_cell_name dsp_dds_compiler_con_0
  if { [catch {set dsp_dds_compiler_con_0 [create_bd_cell -type module -reference $block_name $block_cell_name] } errmsg] } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2095 -severity "ERROR" "Unable to add referenced block <$block_name>. Please add the files for ${block_name}'s definition into the project."}
     return 1
   } elseif { $dsp_dds_compiler_con_0 eq "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2096 -severity "ERROR" "Unable to referenced block <$block_name>. Please add the files for ${block_name}'s definition into the project."}
     return 1
   }
    set_property -dict [ list \
   CONFIG.DATA_WIDTH {16} \
 ] $dsp_dds_compiler_con_0

  # Create interface connections
  connect_bd_intf_net -intf_net Local_oscillator_M_AXIS_DATA [get_bd_intf_pins Local_oscillator/M_AXIS_DATA] [get_bd_intf_pins dsp_dds_compiler_con_0/s_axis]

  # Create port connections
  connect_bd_net -net aclk_0_1 [get_bd_pins adc_clk] [get_bd_pins Local_oscillator/aclk] [get_bd_pins dsp_dds_compiler_con_0/aclk]
  connect_bd_net -net dsp_dds_compiler_con_0_m_axis_tdata [get_bd_pins m_axis_tdata] [get_bd_pins dsp_dds_compiler_con_0/m_axis_tdata]
  connect_bd_net -net dsp_dds_compiler_con_0_m_axis_tvalid [get_bd_pins m_axis_tvalid] [get_bd_pins dsp_dds_compiler_con_0/m_axis_tvalid]
  connect_bd_net -net rst_ni_0_1 [get_bd_pins adc_rst_ni] [get_bd_pins dsp_dds_compiler_con_0/rst_ni]

  # Restore current instance
  current_bd_instance $oldCurInst
}

# Hierarchical cell: data_source_hier
proc create_hier_cell_data_source_hier { parentCell nameHier } {

  variable script_folder

  if { $parentCell eq "" || $nameHier eq "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2092 -severity "ERROR" "create_hier_cell_data_source_hier() - Empty argument(s)!"}
     return
  }

  # Get object for parentCell
  set parentObj [get_bd_cells $parentCell]
  if { $parentObj == "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2090 -severity "ERROR" "Unable to find parent cell <$parentCell>!"}
     return
  }

  # Make sure parentObj is hier blk
  set parentType [get_property TYPE $parentObj]
  if { $parentType ne "hier" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2091 -severity "ERROR" "Parent <$parentObj> has TYPE = <$parentType>. Expected to be <hier>."}
     return
  }

  # Save current instance; Restore later
  set oldCurInst [current_bd_instance .]

  # Set parent object as current
  current_bd_instance $parentObj

  # Create cell and set as current instance
  set hier_obj [create_bd_cell -type hier $nameHier]
  current_bd_instance $hier_obj

  # Create interface pins

  # Create pins
  create_bd_pin -dir I -type clk adc_clk
  create_bd_pin -dir I adc_rst_ni
  create_bd_pin -dir I adc_tvalid_0
  create_bd_pin -dir I -from 1 -to 0 control_in
  create_bd_pin -dir I -from 13 -to 0 data_in_0
  create_bd_pin -dir O -from 31 -to 0 data_out
  create_bd_pin -dir O m_axis_tvalid

  # Create instance: Local_osc_hier
  create_hier_cell_Local_osc_hier $hier_obj Local_osc_hier

  # Create instance: basic_counter_0, and set properties
  set block_name basic_counter
  set block_cell_name basic_counter_0
  if { [catch {set basic_counter_0 [create_bd_cell -type module -reference $block_name $block_cell_name] } errmsg] } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2095 -severity "ERROR" "Unable to add referenced block <$block_name>. Please add the files for ${block_name}'s definition into the project."}
     return 1
   } elseif { $basic_counter_0 eq "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2096 -severity "ERROR" "Unable to referenced block <$block_name>. Please add the files for ${block_name}'s definition into the project."}
     return 1
   }
    set_property -dict [ list \
   CONFIG.DIVIDE_CLK_FREQ_BY {4} \
 ] $basic_counter_0

  # Create instance: dsp_data_source_mux_0, and set properties
  set block_name dsp_data_source_mux
  set block_cell_name dsp_data_source_mux_0
  if { [catch {set dsp_data_source_mux_0 [create_bd_cell -type module -reference $block_name $block_cell_name] } errmsg] } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2095 -severity "ERROR" "Unable to add referenced block <$block_name>. Please add the files for ${block_name}'s definition into the project."}
     return 1
   } elseif { $dsp_data_source_mux_0 eq "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2096 -severity "ERROR" "Unable to referenced block <$block_name>. Please add the files for ${block_name}'s definition into the project."}
     return 1
   }
  
  # Create instance: valid_data_holder_0, and set properties
  set block_name valid_data_holder
  set block_cell_name valid_data_holder_0
  if { [catch {set valid_data_holder_0 [create_bd_cell -type module -reference $block_name $block_cell_name] } errmsg] } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2095 -severity "ERROR" "Unable to add referenced block <$block_name>. Please add the files for ${block_name}'s definition into the project."}
     return 1
   } elseif { $valid_data_holder_0 eq "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2096 -severity "ERROR" "Unable to referenced block <$block_name>. Please add the files for ${block_name}'s definition into the project."}
     return 1
   }
    set_property -dict [ list \
   CONFIG.DATA_LENGTH {16} \
 ] $valid_data_holder_0

  # Create instance: zero_padder_0, and set properties
  set block_name zero_padder
  set block_cell_name zero_padder_0
  if { [catch {set zero_padder_0 [create_bd_cell -type module -reference $block_name $block_cell_name] } errmsg] } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2095 -severity "ERROR" "Unable to add referenced block <$block_name>. Please add the files for ${block_name}'s definition into the project."}
     return 1
   } elseif { $zero_padder_0 eq "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2096 -severity "ERROR" "Unable to referenced block <$block_name>. Please add the files for ${block_name}'s definition into the project."}
     return 1
   }
    set_property -dict [ list \
   CONFIG.LSB_PADDING {false} \
 ] $zero_padder_0

  # Create instance: zero_padder_1, and set properties
  set block_name zero_padder
  set block_cell_name zero_padder_1
  if { [catch {set zero_padder_1 [create_bd_cell -type module -reference $block_name $block_cell_name] } errmsg] } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2095 -severity "ERROR" "Unable to add referenced block <$block_name>. Please add the files for ${block_name}'s definition into the project."}
     return 1
   } elseif { $zero_padder_1 eq "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2096 -severity "ERROR" "Unable to referenced block <$block_name>. Please add the files for ${block_name}'s definition into the project."}
     return 1
   }
    set_property -dict [ list \
   CONFIG.INPUT_WIDTH {14} \
   CONFIG.OUTPUT_WIDTH {16} \
 ] $zero_padder_1

  # Create interface connections
  connect_bd_intf_net -intf_net basic_counter_0_m_axis [get_bd_intf_pins basic_counter_0/m_axis] [get_bd_intf_pins dsp_data_source_mux_0/counter]
  connect_bd_intf_net -intf_net valid_data_holder_0_m_axis [get_bd_intf_pins dsp_data_source_mux_0/adc] [get_bd_intf_pins valid_data_holder_0/m_axis]

  # Create port connections
  connect_bd_net -net aclk_0_1 [get_bd_pins adc_clk] [get_bd_pins Local_osc_hier/adc_clk] [get_bd_pins basic_counter_0/clk_i] [get_bd_pins valid_data_holder_0/clk_i]
  connect_bd_net -net adc_tvalid_0_1 [get_bd_pins adc_tvalid_0] [get_bd_pins valid_data_holder_0/s_axis_tvalid]
  connect_bd_net -net axi_slave_reg_0_data_source_selector [get_bd_pins control_in] [get_bd_pins dsp_data_source_mux_0/control_in]
  connect_bd_net -net data_in_0_1 [get_bd_pins data_in_0] [get_bd_pins zero_padder_1/data_in]
  connect_bd_net -net dsp_data_source_mux_0_m_axis_tdata [get_bd_pins dsp_data_source_mux_0/m_axis_tdata] [get_bd_pins zero_padder_0/data_in]
  connect_bd_net -net dsp_data_source_mux_0_m_axis_tvalid [get_bd_pins m_axis_tvalid] [get_bd_pins dsp_data_source_mux_0/m_axis_tvalid]
  connect_bd_net -net dsp_dds_compiler_con_0_m_axis_tdata [get_bd_pins Local_osc_hier/m_axis_tdata] [get_bd_pins dsp_data_source_mux_0/dds_compiler_tdata]
  connect_bd_net -net dsp_dds_compiler_con_0_m_axis_tvalid [get_bd_pins Local_osc_hier/m_axis_tvalid] [get_bd_pins dsp_data_source_mux_0/dds_compiler_tvalid]
  connect_bd_net -net rst_ni_0_1 [get_bd_pins adc_rst_ni] [get_bd_pins Local_osc_hier/adc_rst_ni] [get_bd_pins basic_counter_0/rst_ni] [get_bd_pins valid_data_holder_0/rst_ni]
  connect_bd_net -net zero_padder_0_data_out [get_bd_pins data_out] [get_bd_pins zero_padder_0/data_out]
  connect_bd_net -net zero_padder_1_data_out [get_bd_pins valid_data_holder_0/s_axis_tdata] [get_bd_pins zero_padder_1/data_out]

  # Restore current instance
  current_bd_instance $oldCurInst
}

# Hierarchical cell: Ch_oscillator_hier
proc create_hier_cell_Ch_oscillator_hier { parentCell nameHier } {

  variable script_folder

  if { $parentCell eq "" || $nameHier eq "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2092 -severity "ERROR" "create_hier_cell_Ch_oscillator_hier() - Empty argument(s)!"}
     return
  }

  # Get object for parentCell
  set parentObj [get_bd_cells $parentCell]
  if { $parentObj == "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2090 -severity "ERROR" "Unable to find parent cell <$parentCell>!"}
     return
  }

  # Make sure parentObj is hier blk
  set parentType [get_property TYPE $parentObj]
  if { $parentType ne "hier" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2091 -severity "ERROR" "Parent <$parentObj> has TYPE = <$parentType>. Expected to be <hier>."}
     return
  }

  # Save current instance; Restore later
  set oldCurInst [current_bd_instance .]

  # Set parent object as current
  current_bd_instance $parentObj

  # Create cell and set as current instance
  set hier_obj [create_bd_cell -type hier $nameHier]
  current_bd_instance $hier_obj

  # Create interface pins

  # Create pins
  create_bd_pin -dir I -type clk adc_clk
  create_bd_pin -dir I adc_rst_ni
  create_bd_pin -dir O -from 31 -to 0 m_axis_tdata

  # Create instance: Channel_selector_oscillator, and set properties
  set Channel_selector_oscillator [ create_bd_cell -type ip -vlnv xilinx.com:ip:dds_compiler:6.0 Channel_selector_oscillator ]
  set_property -dict [ list \
   CONFIG.DATA_Has_TLAST {Not_Required} \
   CONFIG.DDS_Clock_Rate {260} \
   CONFIG.Frequency_Resolution {0.4} \
   CONFIG.Has_Phase_Out {false} \
   CONFIG.Has_TREADY {true} \
   CONFIG.Latency {9} \
   CONFIG.M_DATA_Has_TUSER {Not_Required} \
   CONFIG.Noise_Shaping {None} \
   CONFIG.Output_Frequency1 {0} \
   CONFIG.Output_Width {16} \
   CONFIG.PINC1 {1111110000010} \
   CONFIG.Parameter_Entry {Hardware_Parameters} \
   CONFIG.Phase_Increment {Fixed} \
   CONFIG.Phase_Width {16} \
   CONFIG.S_PHASE_Has_TUSER {Not_Required} \
 ] $Channel_selector_oscillator

  # Create instance: Channel_selector_oscillator_controller, and set properties
  set block_name dsp_dds_compiler_controller
  set block_cell_name Channel_selector_oscillator_controller
  if { [catch {set Channel_selector_oscillator_controller [create_bd_cell -type module -reference $block_name $block_cell_name] } errmsg] } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2095 -severity "ERROR" "Unable to add referenced block <$block_name>. Please add the files for ${block_name}'s definition into the project."}
     return 1
   } elseif { $Channel_selector_oscillator_controller eq "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2096 -severity "ERROR" "Unable to referenced block <$block_name>. Please add the files for ${block_name}'s definition into the project."}
     return 1
   }
    set_property -dict [ list \
   CONFIG.DATA_WIDTH {32} \
   CONFIG.DIVIDE_CLK_FREQ_BY {32} \
 ] $Channel_selector_oscillator_controller

  # Create interface connections
  connect_bd_intf_net -intf_net Oscilador_local_M_AXIS_DATA_1 [get_bd_intf_pins Channel_selector_oscillator/M_AXIS_DATA] [get_bd_intf_pins Channel_selector_oscillator_controller/s_axis]

  # Create port connections
  connect_bd_net -net Channel_selector_oscillator_controller_m_axis_tdata [get_bd_pins m_axis_tdata] [get_bd_pins Channel_selector_oscillator_controller/m_axis_tdata]
  connect_bd_net -net aclk_0_1 [get_bd_pins adc_clk] [get_bd_pins Channel_selector_oscillator/aclk] [get_bd_pins Channel_selector_oscillator_controller/aclk]
  connect_bd_net -net rst_ni_0_1 [get_bd_pins adc_rst_ni] [get_bd_pins Channel_selector_oscillator_controller/rst_ni]

  # Restore current instance
  current_bd_instance $oldCurInst
}

# Hierarchical cell: Ch_filter_hier
proc create_hier_cell_Ch_filter_hier { parentCell nameHier } {

  variable script_folder

  if { $parentCell eq "" || $nameHier eq "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2092 -severity "ERROR" "create_hier_cell_Ch_filter_hier() - Empty argument(s)!"}
     return
  }

  # Get object for parentCell
  set parentObj [get_bd_cells $parentCell]
  if { $parentObj == "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2090 -severity "ERROR" "Unable to find parent cell <$parentCell>!"}
     return
  }

  # Make sure parentObj is hier blk
  set parentType [get_property TYPE $parentObj]
  if { $parentType ne "hier" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2091 -severity "ERROR" "Parent <$parentObj> has TYPE = <$parentType>. Expected to be <hier>."}
     return
  }

  # Save current instance; Restore later
  set oldCurInst [current_bd_instance .]

  # Set parent object as current
  current_bd_instance $parentObj

  # Create cell and set as current instance
  set hier_obj [create_bd_cell -type hier $nameHier]
  current_bd_instance $hier_obj

  # Create interface pins
  create_bd_intf_pin -mode Master -vlnv xilinx.com:interface:axis_rtl:1.0 M_AXIS_DATA_0


  # Create pins
  create_bd_pin -dir I -type clk adc_clk
  create_bd_pin -dir I -from 31 -to 0 data_in
  create_bd_pin -dir I s_axis_data_tvalid

  # Create instance: Channel_filter, and set properties
  set Channel_filter [ create_bd_cell -type ip -vlnv xilinx.com:ip:fir_compiler:7.2 Channel_filter ]
  set_property -dict [ list \
   CONFIG.Clock_Frequency {260} \
   CONFIG.CoefficientSource {COE_File} \
   CONFIG.Coefficient_File {../../../../../../../filters/lowpass.coe} \
   CONFIG.Coefficient_Fractional_Bits {20} \
   CONFIG.Coefficient_Reload {false} \
   CONFIG.Coefficient_Sets {1} \
   CONFIG.Coefficient_Sign {Signed} \
   CONFIG.Coefficient_Structure {Inferred} \
   CONFIG.Coefficient_Width {16} \
   CONFIG.ColumnConfig {1} \
   CONFIG.DATA_Has_TLAST {Not_Required} \
   CONFIG.Data_Fractional_Bits {0} \
   CONFIG.Data_Width {16} \
   CONFIG.Decimation_Rate {50} \
   CONFIG.Filter_Architecture {Systolic_Multiply_Accumulate} \
   CONFIG.Filter_Type {Decimation} \
   CONFIG.Interpolation_Rate {1} \
   CONFIG.M_DATA_Has_TUSER {Not_Required} \
   CONFIG.Number_Channels {1} \
   CONFIG.Number_Paths {2} \
   CONFIG.Output_Rounding_Mode {Full_Precision} \
   CONFIG.Output_Width {37} \
   CONFIG.Quantization {Quantize_Only} \
   CONFIG.RateSpecification {Frequency_Specification} \
   CONFIG.S_DATA_Has_FIFO {true} \
   CONFIG.S_DATA_Has_TUSER {Not_Required} \
   CONFIG.Sample_Frequency {8.125} \
   CONFIG.Select_Pattern {All} \
   CONFIG.Zero_Pack_Factor {1} \
 ] $Channel_filter

  # Create instance: dsp_complex_gain_1, and set properties
  set block_name dsp_complex_gain
  set block_cell_name dsp_complex_gain_1
  if { [catch {set dsp_complex_gain_1 [create_bd_cell -type module -reference $block_name $block_cell_name] } errmsg] } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2095 -severity "ERROR" "Unable to add referenced block <$block_name>. Please add the files for ${block_name}'s definition into the project."}
     return 1
   } elseif { $dsp_complex_gain_1 eq "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2096 -severity "ERROR" "Unable to referenced block <$block_name>. Please add the files for ${block_name}'s definition into the project."}
     return 1
   }
    set_property -dict [ list \
   CONFIG.SHIFT_BY {2} \
 ] $dsp_complex_gain_1

  # Create interface connections
  connect_bd_intf_net -intf_net Conn1 [get_bd_intf_pins M_AXIS_DATA_0] [get_bd_intf_pins Channel_filter/M_AXIS_DATA]

  # Create port connections
  connect_bd_net -net Channel_mixer_m_axis_dout_tdata [get_bd_pins data_in] [get_bd_pins dsp_complex_gain_1/data_in]
  connect_bd_net -net Channel_mixer_m_axis_dout_tvalid [get_bd_pins s_axis_data_tvalid] [get_bd_pins Channel_filter/s_axis_data_tvalid]
  connect_bd_net -net aclk_0_1 [get_bd_pins adc_clk] [get_bd_pins Channel_filter/aclk]
  connect_bd_net -net dsp_complex_gain_1_data_out [get_bd_pins Channel_filter/s_axis_data_tdata] [get_bd_pins dsp_complex_gain_1/data_out]

  # Restore current instance
  current_bd_instance $oldCurInst
}

# Hierarchical cell: Band_filter_hier
proc create_hier_cell_Band_filter_hier { parentCell nameHier } {

  variable script_folder

  if { $parentCell eq "" || $nameHier eq "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2092 -severity "ERROR" "create_hier_cell_Band_filter_hier() - Empty argument(s)!"}
     return
  }

  # Get object for parentCell
  set parentObj [get_bd_cells $parentCell]
  if { $parentObj == "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2090 -severity "ERROR" "Unable to find parent cell <$parentCell>!"}
     return
  }

  # Make sure parentObj is hier blk
  set parentType [get_property TYPE $parentObj]
  if { $parentType ne "hier" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2091 -severity "ERROR" "Parent <$parentObj> has TYPE = <$parentType>. Expected to be <hier>."}
     return
  }

  # Save current instance; Restore later
  set oldCurInst [current_bd_instance .]

  # Set parent object as current
  current_bd_instance $parentObj

  # Create cell and set as current instance
  set hier_obj [create_bd_cell -type hier $nameHier]
  current_bd_instance $hier_obj

  # Create interface pins

  # Create pins
  create_bd_pin -dir I -type clk adc_clk
  create_bd_pin -dir I -from 31 -to 0 data_in
  create_bd_pin -dir O -from 31 -to 0 m_axis_data_tdata
  create_bd_pin -dir O m_axis_data_tvalid
  create_bd_pin -dir I s_axis_data_tvalid

  # Create instance: Band_filter, and set properties
  set Band_filter [ create_bd_cell -type ip -vlnv xilinx.com:ip:fir_compiler:7.2 Band_filter ]
  set_property -dict [ list \
   CONFIG.Clock_Frequency {260} \
   CONFIG.CoefficientSource {COE_File} \
   CONFIG.Coefficient_File {../../../../../../../filters/bandpass.coe} \
   CONFIG.Coefficient_Fractional_Bits {19} \
   CONFIG.Coefficient_Sets {1} \
   CONFIG.Coefficient_Sign {Signed} \
   CONFIG.Coefficient_Structure {Inferred} \
   CONFIG.Coefficient_Width {16} \
   CONFIG.ColumnConfig {3} \
   CONFIG.Data_Fractional_Bits {0} \
   CONFIG.Data_Width {16} \
   CONFIG.Decimation_Rate {8} \
   CONFIG.Filter_Architecture {Systolic_Multiply_Accumulate} \
   CONFIG.Filter_Type {Decimation} \
   CONFIG.Interpolation_Rate {1} \
   CONFIG.Number_Channels {1} \
   CONFIG.Number_Paths {2} \
   CONFIG.Output_Rounding_Mode {Truncate_LSBs} \
   CONFIG.Output_Width {16} \
   CONFIG.Quantization {Quantize_Only} \
   CONFIG.RateSpecification {Frequency_Specification} \
   CONFIG.Sample_Frequency {65} \
   CONFIG.Zero_Pack_Factor {1} \
 ] $Band_filter

  # Create instance: dsp_complex_gain_0, and set properties
  set block_name dsp_complex_gain
  set block_cell_name dsp_complex_gain_0
  if { [catch {set dsp_complex_gain_0 [create_bd_cell -type module -reference $block_name $block_cell_name] } errmsg] } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2095 -severity "ERROR" "Unable to add referenced block <$block_name>. Please add the files for ${block_name}'s definition into the project."}
     return 1
   } elseif { $dsp_complex_gain_0 eq "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2096 -severity "ERROR" "Unable to referenced block <$block_name>. Please add the files for ${block_name}'s definition into the project."}
     return 1
   }
    set_property -dict [ list \
   CONFIG.SHIFT_BY {2} \
 ] $dsp_complex_gain_0

  # Create port connections
  connect_bd_net -net Band_filter_m_axis_data_tdata [get_bd_pins m_axis_data_tdata] [get_bd_pins Band_filter/m_axis_data_tdata]
  connect_bd_net -net Band_filter_m_axis_data_tvalid [get_bd_pins m_axis_data_tvalid] [get_bd_pins Band_filter/m_axis_data_tvalid]
  connect_bd_net -net Band_mixer_m_axis_dout_tdata [get_bd_pins data_in] [get_bd_pins dsp_complex_gain_0/data_in]
  connect_bd_net -net Band_mixer_m_axis_dout_tvalid [get_bd_pins s_axis_data_tvalid] [get_bd_pins Band_filter/s_axis_data_tvalid]
  connect_bd_net -net aclk_0_1 [get_bd_pins adc_clk] [get_bd_pins Band_filter/aclk]
  connect_bd_net -net dsp_complex_gain_0_data_out [get_bd_pins Band_filter/s_axis_data_tdata] [get_bd_pins dsp_complex_gain_0/data_out]

  # Restore current instance
  current_bd_instance $oldCurInst
}

# Hierarchical cell: AXI_hier
proc create_hier_cell_AXI_hier { parentCell nameHier } {

  variable script_folder

  if { $parentCell eq "" || $nameHier eq "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2092 -severity "ERROR" "create_hier_cell_AXI_hier() - Empty argument(s)!"}
     return
  }

  # Get object for parentCell
  set parentObj [get_bd_cells $parentCell]
  if { $parentObj == "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2090 -severity "ERROR" "Unable to find parent cell <$parentCell>!"}
     return
  }

  # Make sure parentObj is hier blk
  set parentType [get_property TYPE $parentObj]
  if { $parentType ne "hier" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2091 -severity "ERROR" "Parent <$parentObj> has TYPE = <$parentType>. Expected to be <hier>."}
     return
  }

  # Save current instance; Restore later
  set oldCurInst [current_bd_instance .]

  # Set parent object as current
  current_bd_instance $parentObj

  # Create cell and set as current instance
  set hier_obj [create_bd_cell -type hier $nameHier]
  current_bd_instance $hier_obj

  # Create interface pins
  create_bd_intf_pin -mode Slave -vlnv xilinx.com:interface:aximm_rtl:1.0 S00_AXI_0


  # Create pins
  create_bd_pin -dir I -type rst AXI_ARESETN
  create_bd_pin -dir I -type clk AXI_CLK
  create_bd_pin -dir O -from 1 -to 0 data_source_selector

  # Create instance: axi_interconnect_0, and set properties
  set axi_interconnect_0 [ create_bd_cell -type ip -vlnv xilinx.com:ip:axi_interconnect:2.1 axi_interconnect_0 ]
  set_property -dict [ list \
   CONFIG.NUM_MI {1} \
   CONFIG.S00_HAS_REGSLICE {0} \
 ] $axi_interconnect_0

  # Create instance: axi_slave_reg_0, and set properties
  set block_name axi_slave_reg
  set block_cell_name axi_slave_reg_0
  if { [catch {set axi_slave_reg_0 [create_bd_cell -type module -reference $block_name $block_cell_name] } errmsg] } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2095 -severity "ERROR" "Unable to add referenced block <$block_name>. Please add the files for ${block_name}'s definition into the project."}
     return 1
   } elseif { $axi_slave_reg_0 eq "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2096 -severity "ERROR" "Unable to referenced block <$block_name>. Please add the files for ${block_name}'s definition into the project."}
     return 1
   }
  
  # Create interface connections
  connect_bd_intf_net -intf_net S00_AXI_0_1 [get_bd_intf_pins S00_AXI_0] [get_bd_intf_pins axi_interconnect_0/S00_AXI]
  connect_bd_intf_net -intf_net axi_interconnect_0_M00_AXI [get_bd_intf_pins axi_interconnect_0/M00_AXI] [get_bd_intf_pins axi_slave_reg_0/S_AXI]

  # Create port connections
  connect_bd_net -net ACLK_0_2 [get_bd_pins AXI_CLK] [get_bd_pins axi_interconnect_0/ACLK] [get_bd_pins axi_interconnect_0/M00_ACLK] [get_bd_pins axi_interconnect_0/S00_ACLK] [get_bd_pins axi_slave_reg_0/S_AXI_ACLK]
  connect_bd_net -net ARESETN_0_1 [get_bd_pins AXI_ARESETN] [get_bd_pins axi_interconnect_0/ARESETN] [get_bd_pins axi_interconnect_0/M00_ARESETN] [get_bd_pins axi_interconnect_0/S00_ARESETN] [get_bd_pins axi_slave_reg_0/S_AXI_ARESETN]
  connect_bd_net -net axi_slave_reg_0_data_source_selector [get_bd_pins data_source_selector] [get_bd_pins axi_slave_reg_0/data_source_selector]

  # Restore current instance
  current_bd_instance $oldCurInst
}


# Procedure to create entire design; Provide argument to make
# procedure reusable. If parentCell is "", will use root.
proc create_root_design { parentCell } {

  variable script_folder
  variable design_name

  if { $parentCell eq "" } {
     set parentCell [get_bd_cells /]
  }

  # Get object for parentCell
  set parentObj [get_bd_cells $parentCell]
  if { $parentObj == "" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2090 -severity "ERROR" "Unable to find parent cell <$parentCell>!"}
     return
  }

  # Make sure parentObj is hier blk
  set parentType [get_property TYPE $parentObj]
  if { $parentType ne "hier" } {
     catch {common::send_gid_msg -ssname BD::TCL -id 2091 -severity "ERROR" "Parent <$parentObj> has TYPE = <$parentType>. Expected to be <hier>."}
     return
  }

  # Save current instance; Restore later
  set oldCurInst [current_bd_instance .]

  # Set parent object as current
  current_bd_instance $parentObj


  # Create interface ports
  set M_AXIS_DATA_0 [ create_bd_intf_port -mode Master -vlnv xilinx.com:interface:axis_rtl:1.0 M_AXIS_DATA_0 ]
  set_property -dict [ list \
   CONFIG.FREQ_HZ {260000000} \
   ] $M_AXIS_DATA_0

  set S00_AXI_0 [ create_bd_intf_port -mode Slave -vlnv xilinx.com:interface:aximm_rtl:1.0 S00_AXI_0 ]
  set_property -dict [ list \
   CONFIG.ADDR_WIDTH {16} \
   CONFIG.ARUSER_WIDTH {0} \
   CONFIG.AWUSER_WIDTH {0} \
   CONFIG.BUSER_WIDTH {0} \
   CONFIG.DATA_WIDTH {32} \
   CONFIG.HAS_BRESP {1} \
   CONFIG.HAS_BURST {0} \
   CONFIG.HAS_CACHE {0} \
   CONFIG.HAS_LOCK {0} \
   CONFIG.HAS_PROT {1} \
   CONFIG.HAS_QOS {0} \
   CONFIG.HAS_REGION {0} \
   CONFIG.HAS_RRESP {1} \
   CONFIG.HAS_WSTRB {1} \
   CONFIG.ID_WIDTH {0} \
   CONFIG.MAX_BURST_LENGTH {1} \
   CONFIG.NUM_READ_OUTSTANDING {1} \
   CONFIG.NUM_READ_THREADS {1} \
   CONFIG.NUM_WRITE_OUTSTANDING {1} \
   CONFIG.NUM_WRITE_THREADS {1} \
   CONFIG.PROTOCOL {AXI4LITE} \
   CONFIG.READ_WRITE_MODE {READ_WRITE} \
   CONFIG.RUSER_BITS_PER_BYTE {0} \
   CONFIG.RUSER_WIDTH {0} \
   CONFIG.SUPPORTS_NARROW_BURST {0} \
   CONFIG.WUSER_BITS_PER_BYTE {0} \
   CONFIG.WUSER_WIDTH {0} \
   ] $S00_AXI_0


  # Create ports
  set AXI_ARESETN [ create_bd_port -dir I -type rst AXI_ARESETN ]
  set AXI_CLK [ create_bd_port -dir I -type clk AXI_CLK ]
  set adc_clk [ create_bd_port -dir I -type clk -freq_hz 260000000 adc_clk ]
  set adc_rst_ni [ create_bd_port -dir I adc_rst_ni ]
  set adc_tvalid_0 [ create_bd_port -dir I adc_tvalid_0 ]
  set data_in_0 [ create_bd_port -dir I -from 13 -to 0 data_in_0 ]

  # Create instance: AXI_hier
  create_hier_cell_AXI_hier [current_bd_instance .] AXI_hier

  # Create instance: Band_filter_hier
  create_hier_cell_Band_filter_hier [current_bd_instance .] Band_filter_hier

  # Create instance: Band_mixer, and set properties
  set Band_mixer [ create_bd_cell -type ip -vlnv xilinx.com:ip:cmpy:6.0 Band_mixer ]
  set_property -dict [ list \
   CONFIG.ARESETN {true} \
   CONFIG.BPortWidth {16} \
   CONFIG.OutputWidth {16} \
   CONFIG.RoundMode {Truncate} \
 ] $Band_mixer

  # Create instance: Band_selector_oscillator, and set properties
  set Band_selector_oscillator [ create_bd_cell -type ip -vlnv xilinx.com:ip:dds_compiler:6.0 Band_selector_oscillator ]
  set_property -dict [ list \
   CONFIG.Amplitude_Mode {Full_Range} \
   CONFIG.DATA_Has_TLAST {Not_Required} \
   CONFIG.DDS_Clock_Rate {260} \
   CONFIG.Frequency_Resolution {0.4} \
   CONFIG.Has_Phase_Out {false} \
   CONFIG.Has_TREADY {true} \
   CONFIG.Latency {9} \
   CONFIG.M_DATA_Has_TUSER {Not_Required} \
   CONFIG.Noise_Shaping {None} \
   CONFIG.Output_Frequency1 {0} \
   CONFIG.Output_Width {16} \
   CONFIG.PINC1 {100100011011101} \
   CONFIG.Parameter_Entry {Hardware_Parameters} \
   CONFIG.Phase_Increment {Fixed} \
   CONFIG.Phase_Width {16} \
   CONFIG.S_PHASE_Has_TUSER {Not_Required} \
 ] $Band_selector_oscillator

  # Create instance: Ch_filter_hier
  create_hier_cell_Ch_filter_hier [current_bd_instance .] Ch_filter_hier

  # Create instance: Ch_oscillator_hier
  create_hier_cell_Ch_oscillator_hier [current_bd_instance .] Ch_oscillator_hier

  # Create instance: Channel_mixer, and set properties
  set Channel_mixer [ create_bd_cell -type ip -vlnv xilinx.com:ip:cmpy:6.0 Channel_mixer ]
  set_property -dict [ list \
   CONFIG.ARESETN {true} \
   CONFIG.BPortWidth {16} \
   CONFIG.MinimumLatency {6} \
   CONFIG.OutputWidth {16} \
   CONFIG.RoundMode {Truncate} \
 ] $Channel_mixer

  # Create instance: data_source_hier
  create_hier_cell_data_source_hier [current_bd_instance .] data_source_hier

  # Create interface connections
  connect_bd_intf_net -intf_net Ch_filter_hier_M_AXIS_DATA_0 [get_bd_intf_ports M_AXIS_DATA_0] [get_bd_intf_pins Ch_filter_hier/M_AXIS_DATA_0]
  connect_bd_intf_net -intf_net S00_AXI_0_1 [get_bd_intf_ports S00_AXI_0] [get_bd_intf_pins AXI_hier/S00_AXI_0]

  # Create port connections
  connect_bd_net -net ACLK_0_2 [get_bd_ports AXI_CLK] [get_bd_pins AXI_hier/AXI_CLK]
  connect_bd_net -net ARESETN_0_1 [get_bd_ports AXI_ARESETN] [get_bd_pins AXI_hier/AXI_ARESETN]
  connect_bd_net -net Band_filter_m_axis_data_tdata [get_bd_pins Band_filter_hier/m_axis_data_tdata] [get_bd_pins Channel_mixer/s_axis_a_tdata]
  connect_bd_net -net Band_filter_m_axis_data_tvalid [get_bd_pins Band_filter_hier/m_axis_data_tvalid] [get_bd_pins Channel_mixer/s_axis_a_tvalid] [get_bd_pins Channel_mixer/s_axis_b_tvalid]
  connect_bd_net -net Band_mixer_m_axis_dout_tdata [get_bd_pins Band_filter_hier/data_in] [get_bd_pins Band_mixer/m_axis_dout_tdata]
  connect_bd_net -net Band_mixer_m_axis_dout_tvalid [get_bd_pins Band_filter_hier/s_axis_data_tvalid] [get_bd_pins Band_mixer/m_axis_dout_tvalid]
  connect_bd_net -net Band_selector_oscillator_m_axis_data_tdata [get_bd_pins Band_mixer/s_axis_a_tdata] [get_bd_pins Band_selector_oscillator/m_axis_data_tdata]
  connect_bd_net -net Channel_mixer_m_axis_dout_tdata [get_bd_pins Ch_filter_hier/data_in] [get_bd_pins Channel_mixer/m_axis_dout_tdata]
  connect_bd_net -net Channel_mixer_m_axis_dout_tvalid [get_bd_pins Ch_filter_hier/s_axis_data_tvalid] [get_bd_pins Channel_mixer/m_axis_dout_tvalid]
  connect_bd_net -net Channel_selector_oscillator_controller_m_axis_tdata [get_bd_pins Ch_oscillator_hier/m_axis_tdata] [get_bd_pins Channel_mixer/s_axis_b_tdata]
  connect_bd_net -net aclk_0_1 [get_bd_ports adc_clk] [get_bd_pins Band_filter_hier/adc_clk] [get_bd_pins Band_mixer/aclk] [get_bd_pins Band_selector_oscillator/aclk] [get_bd_pins Ch_filter_hier/adc_clk] [get_bd_pins Ch_oscillator_hier/adc_clk] [get_bd_pins Channel_mixer/aclk] [get_bd_pins data_source_hier/adc_clk]
  connect_bd_net -net adc_tvalid_0_1 [get_bd_ports adc_tvalid_0] [get_bd_pins data_source_hier/adc_tvalid_0]
  connect_bd_net -net axi_slave_reg_0_data_source_selector [get_bd_pins AXI_hier/data_source_selector] [get_bd_pins data_source_hier/control_in]
  connect_bd_net -net data_in_0_1 [get_bd_ports data_in_0] [get_bd_pins data_source_hier/data_in_0]
  connect_bd_net -net dsp_data_source_mux_0_m_axis_tvalid [get_bd_pins Band_mixer/s_axis_a_tvalid] [get_bd_pins Band_mixer/s_axis_b_tvalid] [get_bd_pins Band_selector_oscillator/m_axis_data_tready] [get_bd_pins data_source_hier/m_axis_tvalid]
  connect_bd_net -net rst_ni_0_1 [get_bd_ports adc_rst_ni] [get_bd_pins Band_mixer/aresetn] [get_bd_pins Ch_oscillator_hier/adc_rst_ni] [get_bd_pins Channel_mixer/aresetn] [get_bd_pins data_source_hier/adc_rst_ni]
  connect_bd_net -net zero_padder_0_data_out [get_bd_pins Band_mixer/s_axis_b_tdata] [get_bd_pins data_source_hier/data_out]

  # Create address segments
  assign_bd_address -offset 0x00000000 -range 0x00001000 -target_address_space [get_bd_addr_spaces S00_AXI_0] [get_bd_addr_segs AXI_hier/axi_slave_reg_0/S_AXI/reg0] -force


  # Restore current instance
  current_bd_instance $oldCurInst

  validate_bd_design
  save_bd_design
}
# End of create_root_design()


##################################################################
# MAIN FLOW
##################################################################

create_root_design ""



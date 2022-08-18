library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.std_logic_unsigned.all;

entity zero_padder is
  generic (
    INPUT_WIDTH  : natural := 16;
    OUTPUT_WIDTH : natural := 32;
    LSB_PADDING  : boolean := true);
  port (
    aclk              : in std_logic;
    rst_ni            : in std_logic;
    s_axis_tdata_in   : in std_logic_vector(INPUT_WIDTH - 1 downto 0);
    s_axis_tvalid_in  : in std_logic;
    m_axis_tdata_out  : out std_logic_vector(OUTPUT_WIDTH - 1 downto 0);
    m_axis_tvalid_out : out std_logic
  );
end zero_padder;

architecture rtl of zero_padder is
  signal m_axis_tdata_reg : std_logic_vector(OUTPUT_WIDTH - 1 downto 0);
  signal m_axis_tvalid_reg : std_logic;
begin
  process (aclk)
  begin
    if rising_edge(aclk) then
      if rst_ni = '0' then
        m_axis_tdata_reg <= (others => '0');
        m_axis_tvalid_reg <= '0';
      else
        m_axis_tvalid_reg <= s_axis_tvalid_in;
        if LSB_PADDING then
          m_axis_tdata_reg(OUTPUT_WIDTH - 1 downto OUTPUT_WIDTH - INPUT_WIDTH) <= s_axis_tdata_in;
        else
          m_axis_tdata_reg(INPUT_WIDTH - 1 downto 0) <= s_axis_tdata_in;
        end if;
      end if;
    end if;
  end process;
  m_axis_tdata_out <= m_axis_tdata_reg;
  m_axis_tvalid_out <= m_axis_tvalid_reg;
end rtl;

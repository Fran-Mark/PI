library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;

entity contador is
    generic (
        N         : integer := 27;
        LED_COUNT : integer := 4);
    port (
        clk         : in std_logic;
        syn_clr     : in std_logic;
        load_en     : in std_logic;
        load_val    : in unsigned (LED_COUNT - 1 downto 0);
        en          : in std_logic;
        current_val : out std_logic_vector (LED_COUNT - 1 downto 0)
    );
end contador;

architecture Behavioral of contador is
    signal time_count_r : unsigned (N - 1 downto 0) := (others => '0');
    signal tick_r : std_logic := '0';
    signal led_count_r : unsigned(LED_COUNT - 1 downto 0) := (others => '0');
    constant TIME_COUNT_MAX : unsigned(N - 1 downto 0) := to_unsigned(100_000_000,N);
    constant LED_COUNT_MAX : unsigned(LED_COUNT - 1 downto 0) := (others => '1');
begin

    process (clk, syn_clr, en, time_count_r)
    begin
        if (rising_edge (clk)) then
            if (syn_clr = '0') then
                tick_r <= '0';
                time_count_r <= (others => '0');
            else
                tick_r <= '0';
                if (en = '1') then
                    if (time_count_r >= TIME_COUNT_MAX) then
                        time_count_r <= (others => '0');
                        tick_r <= '1';
                    else
                        time_count_r <= time_count_r + 1;
                    end if;
                end if;
            end if;
        end if;
    end process;

    process (clk, syn_clr, load_en, tick_r, led_count_r)
    begin
        if (rising_edge(clk)) then
            if (syn_clr = '0') then
                led_count_r <= (others => '0');
            else
                if (load_en = '1') then
                    led_count_r <= load_val;
                else
                    if (tick_r = '1') then
                        if (led_count_r >= LED_COUNT_MAX) then
                            led_count_r <= (others => '0');
                        else
                            led_count_r <= led_count_r + 1;
                        end if;
                    end if;
                end if;
            end if;
        end if;
    end process;

    current_val <= std_logic_vector(led_count_r);

end Behavioral;

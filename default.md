# cva6 (module)

### Author : Florian Zaruba, ETH Zurich

 Copyright 2017-2019 ETH Zurich and University of Bologna.
 Copyright and related rights are licensed under the Solderpad Hardware
 License, Version 0.51 (the "License"); you may not use this file except in
 compliance with the License.  You may obtain a copy of the License at
 http://solderpad.org/licenses/SHL-0.51. Unless required by applicable law
 or agreed to in writing, software, hardware and materials distributed under
 this License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
 CONDITIONS OF ANY KIND, either express or implied. See the License for the
 specific language governing permissions and limitations under the License.

 Date: 19.03.2017
 Description: CVA6 Top-level module

## Parameters
|Name|Type|Dimension|Default Value|Description|
|-|-|-|-|-|
|CVA6Cfg|config_pkg::cva6_cfg_t||build_config_pkg::build_config( cva6_config_pkg::cva6_cfg )| CVA6 config|
|rvfi_probes_instr_t|type||`RVFI_PROBES_INSTR_T(CVA6Cfg)| RVFI PROBES|
|rvfi_probes_csr_t|type||`RVFI_PROBES_CSR_T(CVA6Cfg)||
|rvfi_probes_t|type||struct packed { logic csr = 0; rvfi_probes_instr_t instr = 0; }||
|axi_ar_chan_t|type||struct packed { logic [CVA6Cfg.AxiIdWidth-1:0] id; logic [CVA6Cfg.AxiAddrWidth-1:0] addr; axi_pkg::len_t len; axi_pkg::size_t size; axi_pkg::burst_t burst; logic lock; axi_pkg::cache_t cache; axi_pkg::prot_t prot; axi_pkg::qos_t qos; axi_pkg::region_t region; logic [CVA6Cfg.AxiUserWidth-1:0] user; }| AXI types|
|axi_aw_chan_t|type||struct packed { logic [CVA6Cfg.AxiIdWidth-1:0] id; logic [CVA6Cfg.AxiAddrWidth-1:0] addr; axi_pkg::len_t len; axi_pkg::size_t size; axi_pkg::burst_t burst; logic lock; axi_pkg::cache_t cache; axi_pkg::prot_t prot; axi_pkg::qos_t qos; axi_pkg::region_t region; axi_pkg::atop_t atop; logic [CVA6Cfg.AxiUserWidth-1:0] user; }||
|axi_w_chan_t|type||struct packed { logic [CVA6Cfg.AxiDataWidth-1:0] data; logic [(CVA6Cfg.AxiDataWidth/8)-1:0] strb; logic last; logic [CVA6Cfg.AxiUserWidth-1:0] user; }||
|b_chan_t|type||struct packed { logic [CVA6Cfg.AxiIdWidth-1:0] id; axi_pkg::resp_t resp; logic [CVA6Cfg.AxiUserWidth-1:0] user; }||
|r_chan_t|type||struct packed { logic [CVA6Cfg.AxiIdWidth-1:0] id; logic [CVA6Cfg.AxiDataWidth-1:0] data; axi_pkg::resp_t resp; logic last; logic [CVA6Cfg.AxiUserWidth-1:0] user; }| AXI types|
|noc_req_t|type||struct packed { axi_aw_chan_t aw; logic aw_valid; axi_w_chan_t w; logic w_valid; logic b_ready; axi_ar_chan_t ar; logic ar_valid; logic r_ready; }||
|noc_resp_t|type||struct packed { logic aw_ready; logic ar_ready; logic w_ready; logic b_valid; b_chan_t b; logic r_valid; r_chan_t r; }||
|acc_cfg_t|type||logic| |
|AccCfg|acc_cfg_t||'0||
|cvxif_req_t|type||cvxif_pkg::cvxif_req_t||
|cvxif_resp_t|type||cvxif_pkg::cvxif_resp_t||

## Ports
|Name|Direction|Type|Dimension|Description|
|-|-|-|-|-|
|clk_i|input|logic|| Subsystem Clock - SUBSYSTEM|
|rst_ni|input|logic|| Asynchronous reset active low - SUBSYSTEM|
|boot_addr_i|input|logic [riscv::VLEN-1:0]|| Reset boot address - SUBSYSTEM|
|hart_id_i|input|logic [riscv::XLEN-1:0]|| Hard ID reflected as CSR - SUBSYSTEM|
|irq_i|input|logic [1:0]|| Level sensitive (async) interrupts - SUBSYSTEM|
|ipi_i|input|logic|| Inter-processor (async) interrupt - SUBSYSTEM|
|time_irq_i|input|logic|| Timer (async) interrupt - SUBSYSTEM|
|debug_req_i|input|logic|| Debug (async) request - SUBSYSTEM|
|rvfi_probes_o|output|rvfi_probes_t|| Probes to build RVFI, can be left open when not used - RVFI|
|cvxif_req_o|output|cvxif_req_t|| CVXIF request - SUBSYSTEM|
|cvxif_resp_i|input|cvxif_resp_t|| CVXIF response - SUBSYSTEM|
|noc_req_o|output|noc_req_t|| noc request, can be AXI or OpenPiton - SUBSYSTEM|
|noc_resp_i|input|noc_resp_t|| noc response, can be AXI or OpenPiton - SUBSYSTEM|

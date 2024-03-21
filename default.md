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
|Parameter|Type|Default Value|Description|
|-|-|-|-|
## Ports
|Port|Direction|Type|Dimension|Description|
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

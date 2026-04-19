Runner
======
Execution engine and utility scripts for Hermes.
See the project root README.md for how to run workflows.

  runner.py                      Workflow engine — calls the Claude API to
                                 execute agent steps in sequence.

  runner_config.json             Engine settings: model, API key variable,
                                 file paths, max tokens.

  di_12_aggregate_data_query.py  DI-12 skill implementation — computes
                                 aggregate summaries of RTSM, CTMS, ERP,
                                 and site inventory data.

  reorder_calculator.py          Reorder point calculator — computes min/max
                                 reorder points using a Poisson-approximated
                                 Normal distribution model.

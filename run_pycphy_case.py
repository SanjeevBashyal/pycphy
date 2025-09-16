#!/usr/bin/env python3
"""
Main script to run OpenFOAM case setup using the pycphy package with config files.

This script demonstrates how to use the pycphy.foamCaseDeveloper module
with the new configuration file structure.

Author: Sanjeev Bashyal
Location: https://github.com/SanjeevBashyal/pycphy
"""

import os
import sys

# Add the current directory to Python path to import pycphy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pycphy.foamCaseDeveloper import FoamCaseManager
from pycphy.foamCaseDeveloper.config import (
    global_config, 
    block_mesh_config, 
    control_config, 
    turbulence_config
)

def main():
    """
    Main function to demonstrate pycphy usage with config files.
    """
    print("=== pycphy: Python Computational Physics ===")
    print("OpenFOAM Case Developer Demo (Config Files)")
    print("Author: Sanjeev Bashyal")
    print("=" * 50)
    
    # Get case name from global config
    case_name = global_config.case_name
    print(f"\nCreating OpenFOAM case: '{case_name}'")
    
    if global_config.verbose_output:
        print(f"Case description: {global_config.case_description}")
        print(f"Author: {global_config.author_name}")
        print(f"Output directory: {global_config.output_directory}")
    
    # Create a case manager
    case_manager = FoamCaseManager(case_name)
    
    # Set up geometry configuration from config file
    print("\nSetting up geometry from config file...")
    if global_config.verbose_output:
        print(f"  - Domain: {block_mesh_config.p0} to {block_mesh_config.p1}")
        print(f"  - Cells: {block_mesh_config.cells}")
        total_cells = block_mesh_config.cells[0] * block_mesh_config.cells[1] * block_mesh_config.cells[2]
        print(f"  - Total cells: {total_cells}")
        volume = (block_mesh_config.p1[0] - block_mesh_config.p0[0]) * \
                 (block_mesh_config.p1[1] - block_mesh_config.p0[1]) * \
                 (block_mesh_config.p1[2] - block_mesh_config.p0[2])
        print(f"  - Volume: {volume:.6f}")
        print(f"  - Patch names: {block_mesh_config.patch_names}")
    
    case_manager.setup_geometry(
        p0=block_mesh_config.p0,
        p1=block_mesh_config.p1,
        cells=block_mesh_config.cells,
        patch_names=block_mesh_config.patch_names,
        scale=block_mesh_config.scale
    )
    
    # Set up control configuration from config file
    print("\nSetting up control parameters from config file...")
    if global_config.verbose_output:
        print(f"  - Solver: {control_config.control_params['application']}")
        print(f"  - Time: {control_config.control_params['startTime']} to {control_config.control_params['endTime']}")
        print(f"  - Time step: {control_config.control_params['deltaT']}")
        print(f"  - Write interval: {control_config.control_params['writeInterval']}")
        print(f"  - Write control: {control_config.control_params['writeControl']}")
        print(f"  - Courant number: {control_config.control_params['maxCo']}")
    
    case_manager.setup_control(control_config.control_params)
    
    # Set up turbulence configuration from config file
    print("\nSetting up turbulence model from config file...")
    sim_type = turbulence_config.SIMULATION_TYPE
    if sim_type == "RAS":
        model_props = turbulence_config.RAS_PROPERTIES
        model_name = model_props.get('RASModel', 'N/A')
    elif sim_type == "LES":
        model_props = turbulence_config.LES_PROPERTIES
        model_name = model_props.get('LESModel', 'N/A')
    elif sim_type == "laminar":
        model_props = turbulence_config.LAMINAR_PROPERTIES
        model_name = "laminar"
    else:
        print(f"Warning: Unknown simulation type '{sim_type}'. Using laminar.")
        sim_type = "laminar"
        model_props = {}
        model_name = "laminar"
    
    if global_config.verbose_output:
        print(f"  - Simulation type: {sim_type}")
        print(f"  - Model: {model_name}")
        print(f"  - Turbulence on: {turbulence_config.turbulenceOn}")
    
    case_manager.setup_turbulence(
        simulation_type=sim_type,
        model_properties=model_props
    )
    
    # Create the complete case
    print(f"\nCreating complete OpenFOAM case...")
    success = case_manager.create_full_case()
    
    if success:
        print(f"\n=== SUCCESS ===")
        print(f"OpenFOAM case '{case_name}' has been created successfully!")
        print(f"\nGenerated files:")
        print(f"  - {os.path.join(case_name, 'system', 'blockMeshDict')}")
        print(f"  - {os.path.join(case_name, 'system', 'controlDict')}")
        print(f"  - {os.path.join(case_name, 'constant', 'turbulenceProperties')}")
        
        if global_config.verbose_output:
            print(f"\nCase information:")
            print(f"  - Description: {global_config.case_description}")
            print(f"  - Author: {global_config.author_name}")
            print(f"  - Created: {global_config.creation_date}")
            print(f"  - Solver: {control_config.control_params['application']}")
            print(f"  - Simulation type: {sim_type}")
        
        print(f"\nYou can now run OpenFOAM commands like:")
        print(f"  cd {case_name}")
        print(f"  blockMesh")
        print(f"  {control_config.control_params['application']}")
        return True
    else:
        print(f"\n=== FAILED ===")
        print(f"OpenFOAM case creation failed!")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

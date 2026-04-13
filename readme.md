# Image Charge Simulation and Validation

This repository contains scripts and notebooks for modeling image charges under various dielectric boundary conditions and verifying the results against known analytical solutions.

## Main Script

- **Image_charge_3d.py**  
  The primary Python script that calculates image charges for different boundary conditions of a dielectric layer. It generates potential and field distributions based on the specified setup.

## Validation Notebooks

- **Sheet_of_charge_v2.ipynb**  
  Used to verify the correctness of the generated image charges by comparing the potential to the known analytical result for a uniformly charged sheet.

- **Sheet_of_charge_v3.ipynb**  
  An updated version of the charge sheet validation notebook with additional checks for numerical accuracy and consistency.

## Electric Field Verification

- **E_field_check.py**  
  Tests the electric field computation by comparing the results with analytical dipole field solutions to confirm correct implementation.

- **E_field_check2.py**  
  An extended version of the electric field test script, providing additional verification across multiple dipole configurations and boundary conditions.

## Notes

These scripts and notebooks together form a robust framework to ensure the accuracy of image charge generation and electric field computations in dielectric boundary problems.

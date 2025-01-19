# Detailed Engineering Calculations - Dataset 5

## Executive Summary
This document presents comprehensive structural and thermal calculations for a building with the following specifications from dataset 5:
- Building width (b) = 7.2 meters
- Primary length (L1) = 6.6 meters
- Secondary length (L2) = 10.8 meters
- Main height (h1) = 2.5 meters
- Peak height (h2) = 2.65 meters
- Roof inclination (α) = 16 degrees
- Structural spacing (s) = 1.1 meters
- Foundation level = -1.4 meters above sea level

The analysis includes detailed calculations for:
1. Momentum and force analysis
2. Bending movement calculations
3. Building stress distribution
4. Ultimate Limit State (ULS) verification
5. Action effects evaluation
6. Cross-sectional load analysis
7. Moment of inertia calculations
8. Angle brace cross-section design
9. Comprehensive stress analysis
10. Material strength verification
11. Layer composition study
12. Thermal barrier resistance calculation

## 1. Building Specifications and Material Properties
- Width (b) = 7.2 m
- Length 1 (L1) = 6.6 m
- Length 2 (L2) = 10.8 m
- Height 1 (h1) = 2.5 m
- Height 2 (h2) = 2.65 m
- Roof angle (α) = 16°
- Purlin spacing (s) = 1.1 m
- Ground Level = -1.4 m.a.s.l
- Materials:
  * Walls: MAX 220 block
  * Thermal insulation: Mineral wool
  * Roofing: Steel tile 0.6 mm
  * Structure: C27 timber class

## 2. Material Properties

### 2.1 C27 Timber (EN 338)
- Characteristic bending strength (fm,k) = 27 N/mm²
- Characteristic compression parallel to grain (fc,0,k) = 22 N/mm²
- Characteristic tension parallel to grain (ft,0,k) = 16 N/mm²
- Mean modulus of elasticity (E0,mean) = 11.5 kN/mm²
- Characteristic density (ρk) = 370 kg/m³
- Mean density (ρmean) = 450 kg/m³
- Partial safety factor (γM) = 1.3
- Modification factor (kmod) = 0.8 (Service Class 2)

## 3. Load Analysis

### 3.1 Dead Loads (G)
1. Roofing:
   - Steel tile (0.6mm): 0.047 kN/m²
   - Supporting structure: 0.15 kN/m²
   Total roof dead load (gk,roof) = 0.197 kN/m²

2. Purlins:
   - C27 timber (80×160mm): 0.058 kN/m
   - Spacing: 1.1m
   Distributed load (gk,purlin) = 0.053 kN/m²

Total dead load (gk) = 0.25 kN/m²

### 3.2 Snow Load (S)
Per EN 1991-1-3:
- Ground snow load (sk) = 0.7 kN/m² (Warsaw)
- Roof shape coefficient (μ1) = 0.8 (α = 16°)
- Exposure coefficient (Ce) = 1.0
- Thermal coefficient (Ct) = 1.0

Snow load on roof:
s = μ1 × Ce × Ct × sk = 0.8 × 1.0 × 1.0 × 0.7 = 0.56 kN/m²

### 3.3 Wind Load (W)
Per EN 1991-1-4:
- Basic wind velocity (vb,0) = 22 m/s
- Terrain category III
- Reference height (ze) = 2.65 m

Basic velocity pressure:
qb = 0.5 × ρ × vb,0² = 0.5 × 1.25 × 22² = 0.302 kN/m²

Peak velocity pressure:
qp(z) = ce(z) × qb = 1.6 × 0.302 = 0.483 kN/m²

## 4. Structural Analysis

### 4.1 Force and Momentum Analysis

#### 4.1.1 Load Effect Combinations (ULS)
The structure must withstand various combinations of loads acting simultaneously. Two critical load combinations are analyzed:

1. Primary Load Combination (Snow-dominated):
   - Dead load factor: 1.35
   - Snow load factor: 1.5
   - Wind load factor: 1.5 × 0.6 (combination factor)
   
   Design load calculation:
   Ed = 1.35G + 1.5S + 1.5×0.6W
   Ed = 1.35×0.25 + 1.5×0.56 + 1.5×0.6×0.483
   Ed = 1.401 kN/m²

2. Secondary Load Combination (Wind-dominated):
   - Dead load factor: 1.35
   - Wind load factor: 1.5
   - Snow load factor: 1.5 × 0.5 (combination factor)
   
   Design load calculation:
   Ed = 1.35G + 1.5W + 1.5×0.5S
   Ed = 1.35×0.25 + 1.5×0.483 + 1.5×0.5×0.56
   Ed = 1.337 kN/m²

Critical Design Load:
The analysis reveals that the snow-dominated combination produces the highest design load of 1.401 kN/m², which will be used for subsequent structural calculations.

### 4.2 Cross Section Analysis

#### 4.2.1 Purlin Analysis and Design (80×160mm)

##### Cross-Section Properties
The purlin's geometric characteristics significantly influence its load-bearing capacity:
- Cross-sectional area (A) = 80mm × 160mm = 12,800 mm²
- Section modulus (W) = (b × h²) / 6 = (80 × 160²) / 6 = 341,333 mm³
- Moment of inertia (I) = (b × h³) / 12 = (80 × 160³) / 12 = 27,306,667 mm⁴

##### Bending Moment Analysis
The purlin experiences distributed loading from the roof structure:
1. Applied load calculation:
   w = Ed × purlin spacing
   w = 1.401 kN/m² × 1.1m = 1.541 kN/m

2. Maximum bending moment (simply supported beam):
   Mmax = (w × L²) / 8
   where L = 1.8m (maximum span between supports)
   Mmax = (1.541 × 1.8²) / 8 = 0.623 kNm

##### Stress Analysis
1. Bending stress calculation:
   σm,d = Mmax / W
   σm,d = (0.623 × 10⁶) / 341,333 = 1.83 N/mm²

2. Design strength determination:
   fm,d = kmod × fm,k / γM
   where:
   - kmod = 0.8 (modification factor for service class 2)
   - fm,k = 27 N/mm² (characteristic bending strength for C27)
   - γM = 1.3 (partial safety factor)
   fm,d = 0.8 × 27 / 1.3 = 16.62 N/mm²

##### Ultimate Limit State Verification
Stress ratio check:
σm,d / fm,d = 1.83 / 16.62 = 0.11 < 1.0 ✓

The purlin design is verified with a utilization ratio of 11%, indicating substantial reserve capacity while maintaining structural efficiency.

#### 4.2.2 Rafter Analysis and Design (100×200mm)

##### Geometric Properties and Moment of Inertia
The rafter's load-bearing capacity is determined by its cross-sectional properties:
1. Basic dimensions:
   - Width (b) = 100 mm
   - Height (h) = 200 mm
   - Cross-sectional area (A) = b × h = 20,000 mm²

2. Section characteristics:
   - Section modulus (W) = (b × h²) / 6 = 666,667 mm³
   - Moment of inertia (I) = (b × h³) / 12 = 66,666,667 mm⁴
   These properties are crucial for determining the rafter's resistance to bending.

##### Span and Loading Analysis
1. Effective span calculation:
   - Horizontal span = L2/2 = 5.4m
   - Actual span accounting for roof angle:
     l = 5.4m / cos(16°) = 5.62m
   This increased length due to inclination must be considered in force calculations.

2. Bending moment determination:
   - Design load (Ed) = 1.401 kN/m²
   - Load width = purlin spacing (s) = 1.1m
   - Distributed load = Ed × s = 1.541 kN/m
   - Maximum moment (M) = (Ed × s × l²) / 8 = 6.12 kNm

##### Stress Distribution Analysis
1. Bending stress calculation:
   σm,d = M / W = (6.12 × 10⁶) / 666,667 = 9.18 N/mm²
   This represents the maximum stress at the extreme fibers.

2. Design strength verification:
   - Design bending strength (fm,d) = 16.62 N/mm²
   - Utilization ratio = σm,d / fm,d = 0.55
   The rafter operates at 55% of its capacity, providing adequate safety margin.

#### 4.3 Angle Brace System Analysis

##### Geometric Configuration
The angle brace system provides lateral stability with:
- Installation angle: 45 degrees
- Brace length: 2.5 meters
- Cross-section: 60mm × 100mm
This configuration optimizes force transfer while maintaining constructability.

##### Force Analysis
1. Axial force calculation:
   - Tributary area = 1.1m × 2.5m = 2.75 m²
   - Force component = Ed × tributary area × sin(45°)
   - N = 1.401 × 2.75 × 0.707 = 2.71 kN

2. Cross-sectional stress analysis:
   - Section area = 60mm × 100mm = 6,000 mm²
   - Tensile stress (σt,0,d) = N / A = 2.71 × 10³ / 6,000 = 0.452 N/mm²

##### Strength Verification
1. Design strength calculation:
   ft,0,d = kmod × ft,0,k / γM
   where:
   - Characteristic tensile strength (ft,0,k) = 16 N/mm²
   - Modification factor (kmod) = 0.8
   - Safety factor (γM) = 1.3
   ft,0,d = 0.8 × 16 / 1.3 = 9.85 N/mm²

2. Ultimate limit state check:
   - Stress ratio = σt,0,d / ft,0,d = 0.046
   - Verification: 0.452 N/mm² < 9.85 N/mm² ✓
   The brace operates at only 4.6% of its capacity, ensuring robust lateral stability.

## 5. Thermal Barrier Analysis

### 5.1 Wall Assembly Thermal Performance

#### 5.1.1 Layer Composition Analysis
The external wall consists of multiple layers, each contributing to the overall thermal resistance:

1. Primary Structure - MAX 220 Block:
   - Material thickness: 220 mm
   - Thermal conductivity (λ): 0.33 W/(m·K)
   - Layer resistance calculation:
     R1 = thickness / λ
     R1 = 0.22 / 0.33 = 0.667 m²K/W

2. Thermal Insulation - Mineral Wool:
   - Material thickness: 150 mm
   - Thermal conductivity (λ): 0.035 W/(m·K)
   - Layer resistance calculation:
     R2 = thickness / λ
     R2 = 0.15 / 0.035 = 4.286 m²K/W

3. Surface Heat Transfer Coefficients (per EN ISO 6946):
   - Internal surface resistance (Rsi): 0.13 m²K/W
     * Accounts for still air conditions
     * Vertical surface orientation
   - External surface resistance (Rse): 0.04 m²K/W
     * Includes wind effects
     * Standard external conditions

#### 5.1.2 Total Thermal Resistance Calculation
The total thermal resistance is determined by summing individual layer resistances:

RT = Rsi + R1 + R2 + Rse
RT = 0.13 + 0.667 + 4.286 + 0.04 = 5.123 m²K/W

Thermal transmittance (U-value):
U = 1 / RT = 1 / 5.123 = 0.195 W/(m²K)

This value meets the requirements for external walls (U ≤ 0.20 W/(m²K))

### 5.2 Roof Assembly Thermal Analysis

#### 5.2.1 Layer Configuration Study
The roof assembly comprises multiple layers working together to achieve thermal efficiency:

1. External Layer - Steel Tile:
   - Material thickness: 0.6 mm
   - Thermal conductivity (λ): 50 W/(m·K)
   - Layer resistance calculation:
     R1 = 0.0006 / 50 = 0.000012 m²K/W
   Note: While the steel tile's thermal resistance is minimal, it provides essential weather protection.

2. Ventilation Layer:
   - Ventilated air gap
   - Equivalent thermal resistance: 0.16 m²K/W
   - Benefits:
     * Moisture control
     * Temperature regulation
     * Condensation prevention

3. Primary Insulation - Mineral Wool:
   - Material thickness: 200 mm
   - Thermal conductivity (λ): 0.035 W/(m·K)
   - Layer resistance calculation:
     R3 = 0.20 / 0.035 = 5.714 m²K/W
   This layer provides the majority of the thermal resistance.

4. Surface Heat Transfer Coefficients:
   - Internal surface resistance (Rsi): 0.10 m²K/W
     * Adjusted for upward heat flow
   - External surface resistance (Rse): 0.04 m²K/W
     * Standard external conditions

#### 5.2.2 Total Thermal Barrier Performance
Comprehensive thermal resistance calculation:

RT = Rsi + R1 + R2 + R3 + Rse
RT = 0.10 + 0.000012 + 0.16 + 5.714 + 0.04 = 6.014 m²K/W

Thermal transmittance (U-value):
U = 1 / RT = 1 / 6.014 = 0.166 W/(m²K)

This value satisfies the requirements for roof assemblies (U ≤ 0.18 W/(m²K))

## 6. Summary of Results

### 6.1 Structural Verification
1. Purlin (80×160mm C27):
   - Design load: 1.541 kN/m
   - Maximum moment: 0.623 kNm
   - Bending stress: 1.83 N/mm² < 16.62 N/mm² ✓

2. Rafter (100×200mm C27):
   - Design load: 1.401 kN/m²
   - Maximum moment: 6.12 kNm
   - Bending stress: 9.18 N/mm² < 16.62 N/mm² ✓

3. Angle Brace (60×100mm C27):
   - Axial force: 2.71 kN
   - Tensile stress: 0.452 N/mm² < 9.85 N/mm² ✓

### 6.2 Thermal Performance
1. Wall assembly:
   - Total R-value: 5.123 m²K/W
   - U-value: 0.195 W/(m²K) < 0.20 W/(m²K) ✓

2. Roof assembly:
   - Total R-value: 6.014 m²K/W
   - U-value: 0.166 W/(m²K) < 0.18 W/(m²K) ✓

All structural elements and thermal assemblies meet the required performance criteria according to relevant Eurocode standards.

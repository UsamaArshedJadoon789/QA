# Structural and Thermal Calculations - Dataset 5

## 1. Roof Structure Calculations

### 1.1 Basic Parameters
- Building width (b) = 7.2 m
- Length 1 (L1) = 6.6 m
- Length 2 (L2) = 10.8 m
- Roof angle (α) = 16°
- Purlin spacing (s) = 1.1 m
- Timber class: C27

### 1.2 Material Properties (C27 Timber per EN 338)
- Characteristic bending strength (fm,k) = 27 N/mm²
- Characteristic compression parallel to grain (fc,0,k) = 22 N/mm²
- Mean modulus of elasticity (E0,mean) = 11.5 kN/mm²
- Characteristic density (ρk) = 370 kg/m³
- Partial safety factor (γM) = 1.3 (per EN 1995-1-1)
- Modification factor (kmod) = 0.8 (Service Class 2, medium-term load)

### 1.3 Load Calculations

#### 1.3.1 Dead Loads
1. Steel tile roofing (0.6mm):
   - Weight = 0.047 kN/m²
2. Timber structure (estimated):
   - Rafters = 0.15 kN/m²
   - Purlins = 0.10 kN/m²
Total dead load (gk) = 0.297 kN/m²

#### 1.3.2 Snow Load (per EN 1991-1-3)
For Warsaw, Poland:
- Ground snow load (sk) = 0.7 kN/m²
- Roof shape coefficient (μ1) = 0.8 (α = 16°)
- Exposure coefficient (Ce) = 1.0
- Thermal coefficient (Ct) = 1.0
Snow load on roof (s) = μ1 × Ce × Ct × sk
s = 0.8 × 1.0 × 1.0 × 0.7 = 0.56 kN/m²

#### 1.3.3 Wind Load (per EN 1991-1-4)
Basic parameters for Warsaw:
- Basic wind velocity (vb,0) = 22 m/s
- Terrain category III
- Reference height (ze) = h2 = 2.65 m

Wind pressure calculation:
qp(z) = ce(z) × qb
where:
- ce(z) = 1.6 (exposure factor for z = 2.65m, terrain III)
- qb = 0.5 × ρ × vb,0² = 0.5 × 1.25 × 22² = 0.302 kN/m²
Peak velocity pressure:
qp(z) = 1.6 × 0.302 = 0.483 kN/m²

### 1.4 Purlin Design

#### 1.4.1 Load Transfer
- Design load from roof (Ed) = 1.401 kN/m²
- Purlin spacing (s) = 1.1 m
- Load per purlin = 1.401 × 1.1 = 1.541 kN/m

#### 1.4.2 Section Design
Assuming C27 timber purlin:
- Initial section: 80mm × 160mm
- Maximum span: 1.8m (between rafters)

Design bending moment:
M = (w × l²) / 8
where:
- w = 1.541 kN/m
- l = 1.8m

M = (1.541 × 1.8²) / 8 = 0.623 kNm

Bending stress check:
σm,d = M / W ≤ fm,d
where:
- W = (b × h²) / 6 = (80 × 160²) / 6 = 341,333 mm³
- fm,d = kmod × fm,k / γM = 0.8 × 27 / 1.3 = 16.62 N/mm²

σm,d = 0.623 × 10⁶ / 341,333 = 1.83 N/mm² < 16.62 N/mm² ✓

### 1.5 Rafter Design

#### 1.5.1 Load Combination (ULS)
Per EN 1990:
Ed = 1.35 × gk + 1.5 × qk + 1.5 × ψ0 × qw
where:
- gk = 0.297 kN/m²
- qk (snow) = 0.56 kN/m²
- qw (wind) = 0.483 kN/m²
- ψ0 = 0.6 (wind)

Ed = 1.35 × 0.297 + 1.5 × 0.56 + 1.5 × 0.6 × 0.483
Ed = 1.401 kN/m²

#### 1.4.2 Rafter Section Design
Assuming C27 timber rafter:
- Initial section: 100mm × 200mm
- Spacing: 1.1m

Design bending moment:
M = (Ed × s × l²) / 8
where l = rafter length for worst case span (L2/2)
l = 5.4m / cos(16°) = 5.62m

M = (1.401 × 1.1 × 5.62²) / 8 = 6.12 kNm

Bending stress check:
σm,d = M / W ≤ fm,d
where:
- W = (b × h²) / 6 = (100 × 200²) / 6 = 666,667 mm³
- fm,d = kmod × fm,k / γM = 0.8 × 27 / 1.3 = 16.62 N/mm²

σm,d = 6.12 × 10⁶ / 666,667 = 9.18 N/mm² < 16.62 N/mm² ✓

### 1.5 Wood Column Design

#### 1.5.1 Column Load
Tributary area = 1.1m × 5.4m = 5.94 m²
Total design load:
Ned = Ed × tributary area = 1.401 × 5.94 = 8.32 kN

#### 1.5.2 Column Section
Proposed section: 150mm × 150mm
Area = 22,500 mm²

Compressive stress:
σc,0,d = Ned / A = 8.32 × 10³ / 22,500 = 0.37 N/mm²

Design compressive strength:
fc,0,d = kmod × fc,0,k / γM = 0.8 × 22 / 1.3 = 13.54 N/mm²

0.37 N/mm² < 13.54 N/mm² ✓

## 2. Design Assumptions and Standards

### 2.1 General Assumptions
1. Location: Warsaw, Poland
   - Snow load zone according to EN 1991-1-3
   - Wind load parameters for terrain category III
2. Load Duration Classes (EN 1995-1-1):
   - Dead loads: permanent
   - Snow loads: medium-term
   - Wind loads: short-term
3. Service Class 2 (covered, heated building)
4. Material partial safety factors:
   - γM = 1.3 for timber (EN 1995-1-1)
5. Load combination factors (EN 1990):
   - ψ0 = 0.6 for wind loads
   - ψ0 = 0.5 for snow loads

### 2.2 Material Properties
1. C27 Timber (EN 338):
   - fm,k = 27 N/mm²
   - fc,0,k = 22 N/mm²
   - E0,mean = 11.5 kN/mm²
   - ρk = 370 kg/m³
2. Max 220 Block:
   - Thickness = 220 mm
   - λ = 0.33 W/(m·K)
3. Mineral Wool:
   - λ = 0.035 W/(m·K)
4. Steel Tile:
   - Thickness = 0.6 mm
   - λ = 50 W/(m·K)

## 3. Thermal Insulation Calculations

### 3.1 Wall Assembly (Max 220 block + mineral wool)

#### 2.1.1 Component Properties
1. Max 220 block:
   - Thickness = 220 mm
   - λ = 0.33 W/(m·K)
   R1 = 0.22 / 0.33 = 0.667 m²K/W

2. Mineral wool:
   - Thickness = 150 mm
   - λ = 0.035 W/(m·K)
   R2 = 0.15 / 0.035 = 4.286 m²K/W

3. Surface resistances (per EN ISO 6946):
   - Rsi = 0.13 m²K/W (internal)
   - Rse = 0.04 m²K/W (external)

Total thermal resistance:
RT = Rsi + R1 + R2 + Rse
RT = 0.13 + 0.667 + 4.286 + 0.04 = 5.123 m²K/W

U-value = 1 / RT = 0.195 W/(m²K)

This meets typical requirements for external walls in Poland (U ≤ 0.20 W/(m²K))

### 2.2 Roof Assembly

#### 2.2.1 Component Properties
1. Steel tile:
   - Thickness = 0.6 mm
   - λ = 50 W/(m·K)
   R1 = 0.0006 / 50 = 0.000012 m²K/W

2. Air gap:
   - R2 = 0.16 m²K/W (ventilated air layer)

3. Mineral wool:
   - Thickness = 200 mm
   - λ = 0.035 W/(m·K)
   R3 = 0.20 / 0.035 = 5.714 m²K/W

4. Surface resistances:
   - Rsi = 0.10 m²K/W (upward heat flow)
   - Rse = 0.04 m²K/W

Total thermal resistance:
RT = Rsi + R1 + R2 + R3 + Rse
RT = 0.10 + 0.000012 + 0.16 + 5.714 + 0.04 = 6.014 m²K/W

U-value = 1 / RT = 0.166 W/(m²K)

This meets typical requirements for roofs in Poland (U ≤ 0.18 W/(m²K))

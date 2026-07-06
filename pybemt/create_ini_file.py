from configparser import ConfigParser

def create_ini_file(ini_path, rpm, v_inf, nblade, dia, hub_radius, radii, chord, pitch_ang_deg, rho, nu):
    """
    Create an INI configuration file for pyBEMT analysis
    
    :param ini_path: Path to the output INI file
    :param rpm: Propeller operating RPM
    :param v_inf: Free-stream velocity (m/s)
    :param nblade: Number of blades
    :param dia: Propeller diameter (m)
    :param hub_radius: Hub radius (m)
    :param radii: List of radial positions
    :param chord: List of chord lengths
    :param pitch_ang_deg: List of pitch angles (degrees)
    :param rho: Fluid density (kg/m^3)
    :param nu: Kinematic viscosity (m^2/s)
    """
    cfg = ConfigParser()
    # Case section
    cfg.add_section('case')
    cfg.set('case', 'rpm', str(rpm))
    cfg.set('case', 'v_inf', str(v_inf))
    # Rotor section
    cfg.add_section('rotor')
    cfg.set('rotor', 'nblades', str(nblade))
    cfg.set('rotor', 'diameter', str(dia))
    cfg.set('rotor', 'radius_hub', str(hub_radius))

    n_sample = len(radii)
    section_str = 'NACA_0015_air' if rho <= 2 else 'NACA_0015_water'
    cfg.set('rotor', 'section', ' '.join([section_str] * n_sample))
    cfg.set('rotor', 'radius', ' '.join([f"{r:.8f}" for r in radii]))
    cfg.set('rotor', 'chord', ' '.join([f"{c:.8f}" for c in chord]))
    cfg.set('rotor', 'pitch', ' '.join([f"{p:.4f}" for p in pitch_ang_deg]))

    cfg.add_section('fluid')
    cfg.set('fluid', 'rho', str(rho))
    cfg.set('fluid', 'mu', str(rho * nu))  # Dynamic viscosity mu = rho * nu

    cfg.add_section('solver')
    cfg.set('solver', 'solver', 'bisect')
    
    with open(ini_path, 'w') as f:
        cfg.write(f)

    return ini_path
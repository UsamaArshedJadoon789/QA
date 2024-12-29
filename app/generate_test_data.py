import json
import gc
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Force Agg backend for better memory usage
# Set matplotlib memory limits
matplotlib.rcParams['agg.path.chunksize'] = 1000
os.environ['MPLBACKEND'] = 'Agg'  # Ensure Agg backend
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Tuple

# Always use /app/results in production for consistency
RESULTS_DIR = Path("/app/results")
VISUALIZATIONS_DIR = RESULTS_DIR / "visualizations"

# Create all required directories with proper permissions
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ensure_directories():
    """Ensure all required directories exist with proper permissions"""
    try:
        # Create main results directory
        RESULTS_DIR.mkdir(exist_ok=True, parents=True)
        
        # Create visualization directories for both models and dimensions
        for model in ['slaughterhouse', 'food_processing']:
            for dim in ['2d', '3d']:
                viz_dir = VISUALIZATIONS_DIR / model / dim
                viz_dir.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created directory: {viz_dir}")
        
        # Set permissions to ensure write access
        os.system(f"chmod -R 777 {RESULTS_DIR}")
        logger.info(f"Set permissions for {RESULTS_DIR}")
    except Exception as e:
        logger.error(f"Error creating directories: {e}")
        raise

# Create directories at startup
ensure_directories()

def run_monte_carlo_simulation(n_iterations: int = 10, n_samples: int = 100) -> Dict:
    """Run Monte Carlo simulation for compliance metrics with memory optimization"""
    results = []
    for _ in range(n_iterations):
        # Use float32 for better compatibility while maintaining decent memory efficiency
        automated_time = np.random.normal(2.0, 0.3, n_samples).astype(np.float32)
        human_time = np.random.normal(3.5, 0.5, n_samples).astype(np.float32)
        
        # Simulate compliance rates with some randomness
        base_compliance_rate = 0.88  # Target ~88% compliance
        compliance_rate = np.clip(np.random.normal(base_compliance_rate, 0.03, n_samples), 0, 1).astype(np.float32)
        compliant = (compliance_rate * n_samples).astype(np.int32)
        non_compliant = n_samples - compliant
        
        # Force garbage collection after each iteration
        gc.collect()
        
        results.append({
            "compliant": compliant.mean(),
            "non_compliant": non_compliant.mean(),
            "automated_time": automated_time.mean(),
            "human_time": human_time.mean()
        })
    
    # Calculate averages and standard deviations and convert to Python native types
    return {
        "compliant": {
            "mean": float(np.mean([r["compliant"] for r in results])),
            "std": float(np.std([r["compliant"] for r in results]))
        },
        "non_compliant": {
            "mean": float(np.mean([r["non_compliant"] for r in results])),
            "std": float(np.std([r["non_compliant"] for r in results]))
        },
        "automated_time": {
            "mean": float(np.mean([r["automated_time"] for r in results])),
            "std": float(np.std([r["automated_time"] for r in results]))
        },
        "human_time": {
            "mean": float(np.mean([r["human_time"] for r in results])),
            "std": float(np.std([r["human_time"] for r in results]))
        }
    }

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Generate Monte Carlo simulation results with extreme memory optimization
logger.info("Starting Monte Carlo simulations...")

def process_condition(model_type: str, condition: int) -> Dict:
    """Process a single condition with memory cleanup"""
    logger.info(f"Running simulation for {model_type} condition {condition}")
    result = run_monte_carlo_simulation()
    
    # Convert numpy types to native Python types for JSON serialization
    serializable_result = {
        key: {
            "mean": float(value["mean"]),
            "std": float(value["std"])
        }
        for key, value in result.items()
    }
    
    # Save result immediately and clear memory
    result_file = RESULTS_DIR / f"{model_type}_condition{condition}.json"
    result_file.write_text(json.dumps(serializable_result))
    
    # Generate visualizations immediately
    for dim in ['2d', '3d']:
        try:
            generate_visualization(
                serializable_result,
                f"{model_type.title()} Condition {condition} Compliance",
                model_type,
                condition,
                dim
            )
        except Exception as e:
            logger.error(f"Error generating visualization for {model_type} {dim} condition {condition}: {e}")
    
    # Clear memory
    gc.collect()
    return serializable_result

# Process slaughterhouse conditions one at a time
slaughterhouse_results = {}
for i in range(1, 7):
    slaughterhouse_results[f"condition{i}"] = process_condition('slaughterhouse', i)
    gc.collect()

# Process food processing conditions one at a time
food_processing_results = {}
for i in range(1, 4):
    food_processing_results[f"condition{i}"] = process_condition('food_processing', i)
    gc.collect()

# Save results
(RESULTS_DIR / "slaughterhouse_results.json").write_text(json.dumps(slaughterhouse_results))
(RESULTS_DIR / "food_processing_results.json").write_text(json.dumps(food_processing_results))

def generate_visualization(data, title, model_type, condition, dimension):
    """Create enhanced visualization with compliance and time comparison"""
    import gc
    gc.collect()  # Force garbage collection before visualization
    plt.clf()  # Clear any existing plots
    plt.close('all')  # Close all figures to free memory
    
    # Ensure visualization directory exists with proper permissions
    viz_dir = VISUALIZATIONS_DIR / model_type / dimension
    viz_dir.mkdir(parents=True, exist_ok=True)
    
    # Set permissions for all parent directories
    current_dir = viz_dir
    while str(current_dir) != '/':
        try:
            os.chmod(str(current_dir), 0o777)
            logger.info(f"Set permissions for directory: {current_dir}")
            current_dir = current_dir.parent
        except Exception as e:
            logger.error(f"Error setting permissions for {current_dir}: {e}")
    
    # Construct filename and ensure parent directory permissions
    filename = viz_dir / f"condition{condition}.png"
    logger.info(f"\n=== Visualization Setup ===")
    logger.info(f"Target file: {filename}")
    logger.info(f"Directory exists: {viz_dir.exists()}")
    logger.info(f"Directory permissions: {oct(os.stat(str(viz_dir)).st_mode)[-3:]}")
    
    # Lower memory usage settings
    plt.rcParams['figure.dpi'] = 100  # Lower DPI
    plt.rcParams['savefig.dpi'] = 100  # Lower save DPI
    plt.rcParams['figure.max_open_warning'] = 10  # Lower figure warning threshold
    
    if "2d" in str(filename):
        plt.figure(figsize=(15, 6))
        
        # Plot 1: Compliance Statistics with Error Bars
        plt.subplot(1, 2, 1)
        compliant = data["compliant"]["mean"]
        non_compliant = data["non_compliant"]["mean"]
        compliant_err = data["compliant"]["std"]
        non_compliant_err = data["non_compliant"]["std"]
        
        plt.bar([1, 2], [compliant, non_compliant],
               yerr=[compliant_err, non_compliant_err],
               capsize=5,
               color=['green', 'red'],
               label=['Compliant', 'Non-Compliant'])
        plt.title(f"{title}\nCompliance Statistics")
        plt.ylabel("Count (with std dev)")
        plt.xticks([1, 2], ['Compliant', 'Non-Compliant'])
        
        # Plot 2: Processing Time Comparison with Error Bars
        plt.subplot(1, 2, 2)
        auto_time = data["automated_time"]["mean"]
        human_time = data["human_time"]["mean"]
        auto_err = data["automated_time"]["std"]
        human_err = data["human_time"]["std"]
        
        plt.bar([1, 2], [auto_time, human_time],
               yerr=[auto_err, human_err],
               capsize=5,
               color=['blue', 'orange'],
               label=['Automated', 'Human'])
        plt.title("Processing Time Comparison")
        plt.ylabel("Time (seconds)")
        plt.xticks([1, 2], ['Automated', 'Human'])
    else:  # 3D visualization
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Data points
        x = [1, 1, 2, 2]  # Categories
        y = [1, 2, 1, 2]  # Time points
        z = [
            data["compliant"]["mean"],
            data["automated_time"]["mean"],
            data["non_compliant"]["mean"],
            data["human_time"]["mean"]
        ]
        
        # Create scatter plot with larger points
        scatter = ax.scatter(x, y, z, c=['g','b','r','orange'], s=100)
        
        # Add connecting lines for better visualization
        ax.plot([1,1], [1,2], [z[0],z[1]], 'gray', alpha=0.5)
        ax.plot([2,2], [1,2], [z[2],z[3]], 'gray', alpha=0.5)
        
        # Customize the plot
        ax.set_title(f"{title}\n3D Visualization")
        ax.set_xlabel('Category')
        ax.set_ylabel('Time Point')
        ax.set_zlabel('Value')
        
        # Set custom tick labels
        ax.set_xticks([1, 2])
        ax.set_xticklabels(['Compliant', 'Non-Compliant'])
        ax.set_yticks([1, 2])
        ax.set_yticklabels(['Metrics', 'Processing'])
        
        # Add a color bar
        plt.colorbar(scatter)
    
    plt.tight_layout()
    try:
        # Save with optimized settings and verify
        plt.savefig(filename, dpi=100, bbox_inches='tight', optimize=True)
        os.chmod(filename, 0o777)  # Ensure file is readable
        
        logger.info(f"\n=== Save Complete ===")
        logger.info(f"Successfully saved visualization: {filename}")
        logger.info(f"File exists: {os.path.exists(filename)}")
        logger.info(f"File size: {os.path.getsize(filename)} bytes")
        logger.info(f"File permissions: {oct(os.stat(filename).st_mode)[-3:]}")
        
    except Exception as e:
        logger.error(f"\n=== Save Failed ===")
        logger.error(f"Failed to save visualization: {filename}")
        logger.error(f"Error: {str(e)}")
        logger.error(f"Current working directory: {os.getcwd()}")
        logger.error(f"Directory listing: {os.listdir(os.path.dirname(filename))}")
        raise
    finally:
        plt.close('all')  # Ensure cleanup even if save fails
        gc.collect()  # Force garbage collection
    plt.close()

# Generate visualizations with memory management and logging
logger.info("Generating visualizations...")

def generate_visualizations_with_cleanup(model_type, results, conditions):
    for condition in range(1, conditions + 1):
        for dim in ['2d', '3d']:
            logger.info(f"Generating {dim} visualization for {model_type} condition {condition}")
            try:
                # Clear all matplotlib memory before each visualization
                plt.clf()
                plt.close('all')
                gc.collect()
                
                # Generate one visualization
                viz_path = str(VISUALIZATIONS_DIR / f"{model_type}/{dim}/condition{condition}.png")
                generate_visualization(
                    results[f"condition{condition}"],
                    f"{model_type.title()} Condition {condition} Compliance",
                    model_type,
                    condition,
                    dim
                )
                logger.info(f"Completed visualization generation for {model_type} {dim} condition {condition}")
                
                # Force cleanup after each visualization
                plt.clf()
                plt.close('all')
                gc.collect()
                
                # Small delay to allow memory cleanup
                import time
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error generating visualization for {model_type} {dim} condition {condition}: {e}")
                # Ensure cleanup even on error
                plt.clf()
                plt.close('all')
                gc.collect()

# Generate visualizations for both models
generate_visualizations_with_cleanup('slaughterhouse', slaughterhouse_results, 6)
generate_visualizations_with_cleanup('food_processing', food_processing_results, 3)

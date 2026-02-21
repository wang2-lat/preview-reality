import typer
from rich.console import Console
from pathlib import Path
from material_simulator import MaterialSimulator
from color_calibrator import ColorCalibrator
from detail_annotator import DetailAnnotator

app = typer.Typer(help="CLI tool to generate realistic product previews and reduce custom order returns")
console = Console()

@app.command()
def simulate_material(
    input_image: Path = typer.Argument(..., help="Input image path"),
    output_image: Path = typer.Argument(..., help="Output image path"),
    material: str = typer.Option("canvas", help="Material type: canvas, paper, fabric")
):
    """Simulate material texture on product image"""
    console.print(f"[cyan]Simulating {material} material effect...[/cyan]")
    simulator = MaterialSimulator()
    simulator.apply_material(str(input_image), str(output_image), material)
    console.print(f"[green]✓ Material preview saved to {output_image}[/green]")

@app.command()
def calibrate_color(
    input_image: Path = typer.Argument(..., help="Input image path"),
    output_image: Path = typer.Argument(..., help="Output comparison image path")
):
    """Generate screen vs print color comparison"""
    console.print("[cyan]Generating color calibration comparison...[/cyan]")
    calibrator = ColorCalibrator()
    calibrator.create_comparison(str(input_image), str(output_image))
    console.print(f"[green]✓ Color comparison saved to {output_image}[/green]")

@app.command()
def annotate_details(
    input_image: Path = typer.Argument(..., help="Input image path"),
    output_image: Path = typer.Argument(..., help="Output annotated image path"),
    threshold: float = typer.Option(0.3, help="Detail detection sensitivity (0-1)")
):
    """Annotate potential detail discrepancies"""
    console.print("[cyan]Analyzing and annotating details...[/cyan]")
    annotator = DetailAnnotator()
    annotator.annotate(str(input_image), str(output_image), threshold)
    console.print(f"[green]✓ Annotated image saved to {output_image}[/green]")

@app.command()
def preview_all(
    input_image: Path = typer.Argument(..., help="Input image path"),
    output_dir: Path = typer.Option("./output", help="Output directory"),
    material: str = typer.Option("canvas", help="Material type")
):
    """Generate complete preview package with all effects"""
    output_dir.mkdir(exist_ok=True)
    
    console.print("[cyan]Generating complete preview package...[/cyan]")
    
    material_out = output_dir / f"material_{material}.png"
    simulate_material(input_image, material_out, material)
    
    color_out = output_dir / "color_comparison.png"
    calibrate_color(input_image, color_out)
    
    detail_out = output_dir / "detail_annotated.png"
    annotate_details(input_image, detail_out)
    
    console.print(f"[green]✓ Complete preview package saved to {output_dir}[/green]")

if __name__ == "__main__":
    app()

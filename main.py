#!/usr/bin/env python3
"""
C to C++ Conversion Agent
A sophisticated tool for converting C projects to modern C++ with intelligent analysis.
"""

import argparse
import sys
import asyncio
from pathlib import Path
from typing import Optional

from src.converter.project_converter import ProjectConverter
from src.config.settings import Settings
from src.utils.logger import setup_logger
from src.ui.cli_interface import CLIInterface

async def main():
    """Main entry point for the C to C++ conversion agent."""
    parser = argparse.ArgumentParser(
        description="Convert C projects to modern C++ with intelligent analysis"
    )
    parser.add_argument(
        "input_path",
        type=str,
        help="Path to the C project directory or file"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Output directory for the converted C++ project"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="LLM API key for intelligent analysis"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4",
        help="LLM model to use (default: gpt-4)"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Enable automatic validation of the conversion"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logger(verbose=args.verbose)
    
    # Initialize settings
    settings = Settings()
    if args.api_key:
        settings.llm_api_key = args.api_key
    if args.model:
        settings.llm_model = args.model
    
    # Validate input path
    input_path = Path(args.input_path)
    if not input_path.exists():
        logger.error(f"Input path does not exist: {input_path}")
        sys.exit(1)
    
    # Determine output path
    output_path = Path(args.output) if args.output else input_path.parent / f"{input_path.name}_cpp"
    
    try:
        # Initialize the converter
        converter = ProjectConverter(settings)
        
        if args.interactive:
            # Run interactive CLI interface
            cli = CLIInterface(converter, logger)
            await cli.run_interactive(input_path, output_path)
        else:
            # Run automated conversion
            logger.info(f"Converting C project: {input_path}")
            logger.info(f"Output directory: {output_path}")
            
            result = await converter.convert_project(
                input_path=input_path,
                output_path=output_path,
                validate=args.validate
            )
            
            if result.success:
                logger.info("✅ Conversion completed successfully!")
                logger.info(f"📁 Output: {result.output_path}")
                
                if result.suggestions:
                    logger.info("\n💡 Improvement Suggestions:")
                    for suggestion in result.suggestions:
                        logger.info(f"  • {suggestion}")
                
                if result.validation_results:
                    logger.info(f"\n🔍 Validation: {result.validation_results.status}")
                    if result.validation_results.issues:
                        logger.warning("Issues found during validation:")
                        for issue in result.validation_results.issues:
                            logger.warning(f"  ⚠️  {issue}")
            else:
                logger.error("❌ Conversion failed!")
                for error in result.errors:
                    logger.error(f"  {error}")
                sys.exit(1)
                
    except KeyboardInterrupt:
        logger.info("\n🛑 Conversion cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
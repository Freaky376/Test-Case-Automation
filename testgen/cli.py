"""
CLI interface for TestGen
"""
import argparse
import sys
from pathlib import Path
from typing import Optional

from . import __version__
from .config import Config
from .prepare import create_batches
from .generate import generate_report


def cmd_prepare(args, config: Config):
    """Handle 'prepare' command"""
    success = create_batches(
        config=config,
        source_dir=args.source or '.',
        batch_size=args.batch_size,
        custom_prompt=None
    )
    return 0 if success else 1


def cmd_generate(args, config: Config):
    """Handle 'generate' command"""
    success = generate_report(
        config=config,
        batches_dir=args.batches_dir,
        output_dir=args.output_dir
    )
    return 0 if success else 1


def cmd_config(args, config: Config):
    """Handle 'config' command"""
    if args.config_action == 'show':
        print("Current Configuration:")
        print("=" * 60)
        print(config.show())
        return 0
    
    elif args.config_action == 'set':
        if not args.key or not args.value:
            print("❌ Error: Both --key and --value are required for 'set'")
            return 1
        
        config.set(args.key, args.value)
        config.save()
        print(f"✓ Set {args.key} = {args.value}")
        return 0
    
    elif args.config_action == 'get':
        if not args.key:
            print("❌ Error: --key is required for 'get'")
            return 1
        
        value = config.get(args.key)
        if value is not None:
            print(f"{args.key} = {value}")
            return 0
        else:
            print(f"❌ Key not found: {args.key}")
            return 1
    
    return 0


def cmd_init(args, config: Config):
    """Handle 'init' command - initialize configuration"""
    config_path = Path.cwd() / 'testgen.config.yaml'
    
    if config_path.exists() and not args.force:
        print(f"⚠️  Configuration file already exists: {config_path}")
        print("   Use --force to overwrite")
        return 1
    
    # Save default config to current directory
    config.config_path = str(config_path)
    config.save()
    
    print(f"✓ Configuration file created: {config_path}")
    print("\nYou can now edit this file or use 'testgen config set' to modify settings.")
    return 0


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='TestGen - Test Case Automation CLI Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  testgen prepare                    Prepare batches from screenshots
  testgen prepare --batch-size 6     Use custom batch size
  testgen generate                   Generate Excel report
  testgen config show                Show current configuration
  testgen config set template.primary /path/to/template.xlsx
  testgen init                       Create config file in current directory
        """
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'TestGen {__version__}'
    )
    
    parser.add_argument(
        '--config',
        help='Path to config file',
        default=None
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Prepare command
    prepare_parser = subparsers.add_parser(
        'prepare',
        help='Prepare batches from screenshots'
    )
    prepare_parser.add_argument(
        '--source',
        help='Source directory containing screenshots (default: current directory)',
        default=None
    )
    prepare_parser.add_argument(
        '--batch-size',
        type=int,
        help='Number of images per batch (overrides config)',
        default=None
    )
    
    # Generate command
    generate_parser = subparsers.add_parser(
        'generate',
        help='Generate Excel report from batches'
    )
    generate_parser.add_argument(
        '--batches-dir',
        help='Directory containing batch folders (overrides config)',
        default=None
    )
    generate_parser.add_argument(
        '--output-dir',
        help='Output directory for Excel report (overrides config)',
        default=None
    )
    
    # Config command
    config_parser = subparsers.add_parser(
        'config',
        help='Manage configuration'
    )
    config_parser.add_argument(
        'config_action',
        choices=['show', 'get', 'set'],
        help='Configuration action'
    )
    config_parser.add_argument(
        '--key',
        help='Configuration key (dot notation, e.g., template.primary)'
    )
    config_parser.add_argument(
        '--value',
        help='Configuration value (for set action)'
    )
    
    # Init command
    init_parser = subparsers.add_parser(
        'init',
        help='Initialize configuration file in current directory'
    )
    init_parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing configuration file'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Load configuration
    try:
        config = Config(config_path=args.config)
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return 1
    
    # Execute command
    try:
        if args.command == 'prepare':
            return cmd_prepare(args, config)
        elif args.command == 'generate':
            return cmd_generate(args, config)
        elif args.command == 'config':
            return cmd_config(args, config)
        elif args.command == 'init':
            return cmd_init(args, config)
        else:
            parser.print_help()
            return 1
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        return 130
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

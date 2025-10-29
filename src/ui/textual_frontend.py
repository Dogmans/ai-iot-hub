"""
Textual Frontend for AI-IoT Hub

Rich terminal interface using Textual framework for enhanced user experience
with formatted AI responses, interactive input, and visual device management.
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Input, RichLog, Button
from textual.binding import Binding
from rich.console import Console
from rich.text import Text
from pathlib import Path
import asyncio
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))


class AIIoTApp(App):
    """AI-IoT Hub with rich Textual interface"""
    
    CSS = """
    Screen {
        layout: vertical;
    }
    
    Header {
        dock: top;
        height: 3;
    }
    
    Footer {
        dock: bottom;
        height: 3;
    }
    
    #main_container {
        height: 1fr;
        layout: vertical;
        padding: 1;
    }
    
    #response_log {
        height: 1fr;
        border: solid $primary;
        margin-bottom: 1;
    }
    
    #input_container {
        height: 3;
        layout: horizontal;
    }
    
    #user_input {
        width: 1fr;
        margin-right: 1;
    }
    
    #send_button {
        width: 10;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
        Binding("ctrl+l", "clear", "Clear"),
        ("enter", "send_message", "Send"),
    ]
    
    def __init__(self):
        super().__init__()
        self.ai_controller = None
        
    def compose(self) -> ComposeResult:
        """Create the UI layout"""
        yield Header(show_clock=True)
        
        with Container(id="main_container"):
            yield RichLog(
                id="response_log",
                highlight=True,
                markup=True,
                wrap=True
            )
            
            with Horizontal(id="input_container"):
                yield Input(
                    placeholder="Ask me to discover devices, control them, or check status...",
                    id="user_input"
                )
                yield Button("Send", id="send_button")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize the AI controller when app starts"""
        self.title = "AI-IoT Hub"
        self.sub_title = "Intelligent Device Communication"
        
        # Initialize AI controller
        try:
            # Fix import path - we need to go up from src/ui to project root
            import sys
            from pathlib import Path
            project_root = Path(__file__).parent.parent.parent
            sys.path.insert(0, str(project_root / 'src'))
            
            from hub.ai_controller import AIDeviceController
            self.ai_controller = AIDeviceController()
            self.log_message("🤖 [bold green]AI Device Controller initialized successfully![/bold green]")
            self.log_message("[dim]💡 Try: 'discover devices' or 'help'[/dim]")
        except Exception as e:
            # Fail clearly instead of misleading demo mode
            self.ai_controller = None
            self.log_message("[bold red]❌ Failed to initialize AI Device Controller[/bold red]")
            self.log_message(f"[dim]Error: {e}[/dim]")
            self.log_message("[dim]Please check your configuration and dependencies.[/dim]")
            self.log_message("[yellow]💡 Solution: Ensure smolagents and all dependencies are installed[/yellow]")
            self.log_message("[dim]Exit and fix the issue before continuing.[/dim]")
    
    def log_message(self, message: str, markup: bool = True):
        """Add message to response log with rich formatting"""
        response_log = self.query_one("#response_log", RichLog)
        if markup:
            # Use Rich Text object to ensure proper markup rendering
            from rich.text import Text
            text_obj = Text.from_markup(message)
            response_log.write(text_obj)
        else:
            # Plain text without markup processing
            response_log.write(message)
    
    async def action_send_message(self) -> None:
        """Handle sending user message"""
        user_input = self.query_one("#user_input", Input)
        message = user_input.value.strip()
        
        if not message:
            return
            
        # Disable input while processing
        user_input.disabled = True
        user_input.placeholder = "🤖 AI is thinking..."
        
        # Clear input
        user_input.value = ""
        
        # Log user message
        self.log_message(f"[bold cyan]You:[/bold cyan] {message}")
        
        # Process with AI
        await self.process_user_message(message)
        
        # Re-enable input
        user_input.disabled = False
        user_input.placeholder = "Ask me to discover devices, control them, or check status..."
    
    async def process_user_message(self, message: str):
        """Process user message with AI controller"""
        # Check if AI controller is available
        if not self.ai_controller:
            self.log_message("[bold red]❌ Cannot process request[/bold red]")
            self.log_message("[dim]AI Device Controller failed to initialize.[/dim]")
            self.log_message("[yellow]Please restart after fixing configuration issues.[/yellow]")
            return
            
        try:
            # Show enhanced thinking indicator with animation
            thinking_msg = "[dim]🧠 [bold]Analyzing your request...[/bold][/dim]"
            self.log_message(thinking_msg)
            
            # Add processing steps for better user feedback
            await asyncio.sleep(0.2)  # Brief pause for visual feedback
            
            # Show what we're doing based on request type
            if any(keyword in message.lower() for keyword in ['discover', 'scan', 'find']):
                self.log_message("[dim]🔍 [bold]Initializing device discovery...[/bold] Checking network tools...[/dim]")
                await asyncio.sleep(0.3)
                self.log_message("[dim]📡 [bold]Scanning network...[/bold] Looking for IoT devices...[/dim]")
            elif any(keyword in message.lower() for keyword in ['control', 'turn', 'set', 'start', 'stop']):
                self.log_message("[dim]🎮 [bold]Preparing device control...[/bold] Loading communication protocols...[/dim]")
                await asyncio.sleep(0.3)
                self.log_message("[dim]🔧 [bold]Generating control code...[/bold] Configuring device interface...[/dim]")
            elif any(keyword in message.lower() for keyword in ['status', 'check', 'info']):
                self.log_message("[dim]📊 [bold]Gathering device data...[/bold] Checking device status...[/dim]")
                await asyncio.sleep(0.3)
                self.log_message("[dim]🔍 [bold]Analyzing information...[/bold] Preparing report...[/dim]")
            else:
                self.log_message("[dim]🤖 [bold]AI agent processing...[/bold] Understanding request...[/dim]")
                await asyncio.sleep(0.3)
                self.log_message("[dim]⚙️ [bold]Executing tools...[/bold] Generating response...[/dim]")
            
            # Get AI response with Textual-specific prompt
            response = await self.get_ai_response(message)
            
            # Show completion with context
            self.log_message("[dim]✅ [bold green]Complete![/bold green] Response generated successfully.[/dim]")
            await asyncio.sleep(0.2)  # Brief pause before showing result
            
            # Display AI response - use separate calls to preserve markup
            self.log_message("[bold green]AI-IoT Hub:[/bold green]")
            self.log_message(response)
            
        except Exception as e:
            self.log_message(f"[bold red]❌ Error:[/bold red] {str(e)}")
    

    async def get_ai_response(self, user_message: str) -> str:
        """Get AI response with Textual markup formatting"""
        
        if self.ai_controller and hasattr(self.ai_controller, 'process_request_with_textual'):
            return await self.ai_controller.process_request_with_textual("", user_message)
        elif self.ai_controller:
            # Fallback for controllers without Textual support
            return await self.ai_controller.process_user_request(user_message)
        else:
            return "[red]❌ AI Controller not available[/red]"
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks"""
        if event.button.id == "send_button":
            asyncio.create_task(self.action_send_message())
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key in input field"""
        asyncio.create_task(self.action_send_message())
    
    def action_clear(self) -> None:
        """Clear the response log"""
        response_log = self.query_one("#response_log", RichLog)
        response_log.clear()
        self.log_message("🧹 [dim]Chat cleared[/dim]")
    
    async def action_quit(self) -> None:
        """Exit the application"""
        self.exit()



def run_textual_app():
    """Run the Textual AI-IoT Hub application"""
    app = AIIoTApp()
    app.run()


if __name__ == "__main__":
    run_textual_app()
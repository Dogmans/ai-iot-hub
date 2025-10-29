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
            from src.hub.ai_controller import AIDeviceController
            self.ai_controller = AIDeviceController()
            self.log_message("🤖 [bold green]AI Device Controller initialized successfully![/bold green]")
            self.log_message("[dim]💡 Try: 'discover devices' or 'help'[/dim]")
        except ImportError as e:
            # Fallback to demo mode
            self.ai_controller = DemoAIController()
            self.log_message("🤖 [bold yellow]AI-IoT Hub (Demo Mode)[/bold yellow] - Ready!")
            self.log_message("[dim]💡 Try: 'discover devices' or 'control washing machine'[/dim]")
    
    def log_message(self, message: str, markup: bool = True):
        """Add message to response log with rich formatting"""
        response_log = self.query_one("#response_log", RichLog)
        response_log.write(message, markup=markup)
    
    async def action_send_message(self) -> None:
        """Handle sending user message"""
        user_input = self.query_one("#user_input", Input)
        message = user_input.value.strip()
        
        if not message:
            return
            
        # Clear input
        user_input.value = ""
        
        # Log user message
        self.log_message(f"[bold cyan]You:[/bold cyan] {message}")
        
        # Process with AI
        await self.process_user_message(message)
    
    async def process_user_message(self, message: str):
        """Process user message with AI controller"""
        try:
            # Show thinking indicator
            self.log_message("[dim]🤔 Processing your request...[/dim]")
            
            # Get AI response with Textual-specific prompt
            response = await self.get_ai_response(message)
            
            # Display AI response
            self.log_message(f"[bold green]AI-IoT Hub:[/bold green]\n{response}")
            
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
    
    def action_quit(self) -> None:
        """Exit the application"""
        self.exit()


class DemoAIController:
    """Demo AI controller for when smolagents isn't available"""
    
    async def process_request_with_textual(self, textual_prompt: str, user_message: str) -> str:
        """Process request and return Textual-formatted response"""
        
        # Simulate processing delay
        await asyncio.sleep(1)
        
        message_lower = user_message.lower()
        
        if "discover" in message_lower or "find" in message_lower:
            return """[bold green]🔍 Device Discovery Complete[/bold green]

Found [yellow]3 devices[/yellow] on network [cyan]192.168.1.0/24[/cyan]:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• [bold]Samsung SmartThings Hub[/bold]
  IP: [cyan]192.168.1.100[/cyan] | Status: [green]🟢 Online[/green]
  Protocol: [code]SmartThings REST API[/code]
  [dim]Last seen: 2 minutes ago[/dim]
  
• [bold]Philips Hue Bridge[/bold] 
  IP: [cyan]192.168.1.101[/cyan] | Status: [green]🟢 Online[/green]
  Protocol: [code]Philips Hue HTTP API[/code]
  [dim]16 lights connected[/dim]
  
• [bold]Modbus Temperature Sensor[/bold]
  IP: [cyan]192.168.1.115[/cyan] | Status: [green]🟢 Online[/green] 
  Protocol: [code]Modbus TCP Port 502[/code]
  [dim]Current: 22.5°C[/dim]

[dim]💡 Try: "control washing machine" or "check temperature sensor"[/dim]"""

        elif "wash" in message_lower or "machine" in message_lower:
            return """[bold green]🌊 Washing Machine Controller[/bold green]

[yellow]Samsung SmartThings Washer[/yellow] at [cyan]192.168.1.100[/cyan]

[bold]Current Status:[/bold]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• State: [green]🟢 Ready[/green]
• Door: [cyan]Closed & Locked[/cyan] 
• Cycle: [dim]None selected[/dim]
• Time Remaining: [dim]--:--[/dim]

[bold]Available Commands:[/bold]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• [code]start normal cycle[/code] - Standard wash (45 min)
• [code]start delicate cycle[/code] - Gentle wash (30 min)  
• [code]start heavy cycle[/code] - Deep clean (60 min)
• [code]check status[/code] - Current state & progress
• [code]stop washing[/code] - Emergency stop

[dim]🔐 Credentials configured automatically via SmartThings[/dim]"""

        elif "temperature" in message_lower or "sensor" in message_lower:
            return """[bold green]🌡️ Temperature Sensor Reading[/bold green]

[yellow]Modbus Temperature Sensor[/yellow] at [cyan]192.168.1.115[/cyan]

[bold]Current Reading:[/bold]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Temperature: [green]22.5°C[/green] ([dim]72.5°F[/dim])
• Humidity: [cyan]45%[/cyan]
• Air Quality: [green]🟢 Good[/green]
• Timestamp: [dim]Just now[/dim]

[bold]Sensor Details:[/bold] 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Protocol: [code]Modbus TCP (Port 502)[/code]
• Register: [code]Holding Register 0x01-0x03[/code]
• Update Rate: [dim]Every 30 seconds[/dim]
• Accuracy: [dim]±0.5°C, ±3% RH[/dim]

[dim]📊 All readings within normal range (18-25°C optimal)[/dim]"""

        elif "help" in message_lower:
            return """[bold green]🤖 AI-IoT Hub Help[/bold green]

[bold]Available Commands:[/bold]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[cyan]🔍 Device Discovery:[/cyan]
• [code]discover devices[/code] - Scan network for IoT devices
• [code]find all devices[/code] - Complete network scan with details
• [code]scan network[/code] - Quick device discovery

[cyan]⚙️ Device Control:[/cyan] 
• [code]control washing machine[/code] - SmartThings washer interface
• [code]start washing machine[/code] - Begin wash cycle
• [code]check thermostat[/code] - Temperature control
• [code]read temperature sensor[/code] - Get current sensor data
• [code]control lights[/code] - Philips Hue bridge control

[cyan]📊 Status & Monitoring:[/cyan]
• [code]device status[/code] - Check all device states  
• [code]network status[/code] - Network connectivity check
• [code]system info[/code] - Hub system information

[cyan]🛠️ Interface:[/cyan]
• [code]help[/code] - Show this help message
• [code]Ctrl+L[/code] - Clear chat history
• [code]Ctrl+C[/code] - Exit application

[dim]💡 Just type naturally - I understand conversational requests![/dim]
[dim]Example: "Turn on the living room lights" or "What's the temperature?"[/dim]"""

        else:
            return f"""[bold yellow]🤔 Understanding Your Request[/bold yellow]

You said: [italic]"{user_message}"[/italic]

[bold]I can help with:[/bold]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• [green]🔍 Device discovery[/green] - Find and identify IoT devices
• [green]⚙️ Device control[/green] - Send commands to your devices  
• [green]📊 Status monitoring[/green] - Check device states and readings
• [green]📚 Documentation[/green] - Learn about protocols and setup

[bold]Popular Commands:[/bold]
• [cyan]"discover devices"[/cyan] - Start here to find your devices
• [cyan]"control washing machine"[/cyan] - SmartThings appliance control
• [cyan]"check temperature"[/cyan] - Read sensor data

[dim]💡 Try: "discover devices" or "help" for complete command list[/dim]"""

    async def process_user_request(self, user_message: str) -> str:
        """Fallback method for basic processing"""
        return await self.process_request_with_textual("", user_message)


def run_textual_app():
    """Run the Textual AI-IoT Hub application"""
    app = AIIoTApp()
    app.run()


if __name__ == "__main__":
    run_textual_app()
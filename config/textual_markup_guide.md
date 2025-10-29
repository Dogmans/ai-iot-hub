# Textual Markup Formatting Guide for AI Responses

## Basic Text Formatting
- `[bold]text[/bold]` - **Bold text** for important information
- `[italic]text[/italic]` - *Italic text* for emphasis
- `[dim]text[/dim]` - Dimmed text for secondary information
- `[code]text[/code]` - Monospace text for file paths, commands, technical details

## Color Formatting
- `[green]text[/green]` - Green for success messages, online status
- `[red]text[/red]` - Red for errors, warnings, offline status
- `[yellow]text[/yellow]` - Yellow for device names, important values, warnings
- `[cyan]text[/cyan]` - Cyan for IP addresses, technical details, parameters
- `[blue]text[/blue]` - Blue for links, secondary actions
- `[magenta]text[/magenta]` - Magenta for special highlights

## Visual Structure
- `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━` - Section dividers (use 40+ chars)
- `• ` - Bullet points for lists
- `  ` - Two spaces for indentation in nested items

## Status Indicators
- `🟢` - Online/Success/Active
- `🔴` - Offline/Error/Inactive  
- `🟡` - Warning/Pending/Partial
- `🔵` - Info/Processing/Neutral

## Common Icons
- `🔍` - Discovery/Search operations
- `📡` - Network/Communication
- `⚙️` - Configuration/Settings
- `🌊` - Washing machine operations
- `🌡️` - Temperature/Sensors
- `💡` - Tips/Suggestions
- `🤖` - AI/System messages
- `🔐` - Security/Credentials
- `📊` - Data/Statistics
- `🧹` - Cleaning/Clearing
- `🚀` - Starting/Launching

## Response Structure Template

```
[bold green]✅ [Action] Complete[/bold green]

[Brief summary with [yellow]highlighted values[/yellow]]

[Optional section divider]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Main content with structured information:]
• [bold]Item Name[/bold] at [cyan]IP Address[/cyan]
  Status: [green]🟢 Status[/green] | Protocol: [code]Protocol Name[/code]
  [dim]Additional details[/dim]

[dim]💡 Next suggestion or tip[/dim]
```

## Example Formatted Response

```
[bold green]🔍 Device Discovery Complete[/bold green]

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

[dim]💡 Try: "control washing machine" or "check temperature sensor"[/dim]
```

## Error Response Template

```
[bold red]❌ [Error Type][/bold red]

[red]Error description here[/red]

[bold]Troubleshooting:[/bold]
• Check that [yellow]specific item[/yellow] is configured
• Verify [cyan]network connectivity[/cyan] 
• Review [code]configuration file[/code]

[dim]💡 Tip: Specific helpful suggestion[/dim]
```

## Guidelines
1. Always start responses with a clear status header using appropriate colors
2. Use consistent spacing and indentation for readability
3. Include relevant emojis but don't overuse them
4. End with helpful next steps or tips in dim text
5. Use section dividers for long responses with multiple sections
6. Highlight important values (IPs, device names, numbers) with appropriate colors
7. Keep technical details in [code] formatting
8. Use bullet points for lists and structured information
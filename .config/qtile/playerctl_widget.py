import subprocess

def get_playerctl_metadata():
    try:
        # Fetch metadata
        metadata = subprocess.check_output(
            [
                "playerctl", "metadata",
                "--format", "{{artist}} - {{title}} : {{status}}"
            ]
        ).decode("utf-8").strip()

        # Fetch position and length directly from metadata
        position_output = subprocess.check_output(
            [
                "playerctl", "metadata",
                "--format", "{{position}}"
            ]
        ).decode("utf-8").strip()

        length_output = subprocess.check_output(
            [
                "playerctl", "metadata",
                "--format", "{{mpris:length}}"
            ]
        ).decode("utf-8").strip()

        # Convert position and length to seconds
        position_seconds = int(float(position_output) / 1000000)
        length_seconds = int(int(length_output) / 1000000)  # Convert microseconds to seconds

        # Format position and length as minutes:seconds
        position_formatted = f"{position_seconds // 60}:{position_seconds % 60:02d}"
        length_formatted = f"{length_seconds // 60}:{length_seconds % 60:02d}"

        # Truncate title if necessary
        parts = metadata.split(" - ")
        if len(parts) > 1:
            title = parts[1]
            if len(title) > 30:
                title = title[:27] + "..."
            parts[1] = title
            metadata = " - ".join(parts)

        # Append progress to metadata
        metadata += f" [{position_formatted} / {length_formatted}]"

        return metadata
    except subprocess.CalledProcessError:
        return "No media playing"

# Example usage
print(get_playerctl_metadata())

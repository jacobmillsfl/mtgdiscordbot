# Forces users to use this file correctly by sourcing it instead of running it via a new bash session
(
  [[ -n $ZSH_VERSION && $ZSH_EVAL_CONTEXT =~ :file$ ]] || 
  [[ -n $KSH_VERSION && "$(cd -- "$(dirname -- "$0")" && pwd -P)/$(basename -- "$0")" != "$(cd -- "$(dirname -- "${.sh.file}")" && pwd -P)/$(basename -- "${.sh.file}")" ]] || 
  [[ -n $BASH_VERSION ]] && (return 0 2>/dev/null)
) && sourced=1 || sourced=0
if [ "$sourced" -eq "0" ]; then
    echo "Usage: source ./initialize_app.sh"
    exit -1
fi


echo "* * * * MTG Discord Bot Environment Initializer * * * *"
echo ""
echo "      This script creates the initial files needed to"
echo "      run this application, including a Python"
echo "      virtual environment."
echo ""
echo "      You do not need to run this script more than once"
echo "      unless Python dependencies change."
echo ""

# Allow user to specify custom environment variables

read -p "Enter Discord Auth Token (default: \"\"): " discord_auth_token
if [[ -z "$discord_auth_token" ]]; then
    discord_auth_token=""
    echo "Using empty string for Discord Auth Token"
fi

if [ -d "./mtgbot" ]; then
    echo "Using existing Python environment: mtgbot"
else
    echo "Creating new Python environment: mtgbot"
    python3 -m venv mtgbot
fi

echo "Installing Python dependencies..."
source mtgbot/bin/activate
python3 -m pip install -r requirements.txt
echo "Python virtual environment activated and initialized!"
echo "To deactivate, enter: deactivate"

if [ -f "./.mtgbot.env" ]; then
    echo "Using existing Python environment file: .mtgbot.env"
else
    echo "Creating environment file: .mtgbot.env"
cat << EOF > .mtgbot.env
DISCORD_AUTH_TOKEN="$discord_auth_token"
CHANNEL_ID=""
EOF
fi

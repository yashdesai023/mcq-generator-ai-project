# To learn more about how to configure your Nix environment,
# see: https://developers.google.com/idx/guides/customize-idx-env
{ pkgs, ... }: {
  channel = "stable-24.05";

  # We only need the base Python interpreter from Nix.
  packages = [
    pkgs.python311
  ];

  idx = {
    extensions = [
      "ms-python.python"
    ];

    workspace = {
      # This block automates your Python project setup.
      onCreate = {
        # 1. Create a virtual environment named .venv in your project folder.
        create-venv = "python3 -m venv .venv";
        # 2. Activate the venv and install all packages from your requirements.txt.
        install-packages = ". .venv/bin/activate && pip install --no-cache-dir -r requirements.txt";
      };

      onStart = {
        # A reminder for you when you open a new terminal.
        welcome-message = "echo 'Welcome back! Your Python environment is in .venv. To activate it in a new terminal, run: source .venv/bin/activate'";
      };
    };

    previews = {
      enable = true;
      previews = {
        web = {
          # UPDATED COMMAND: Added flags to make Streamlit work behind a proxy.
          command = ["bash" "-c" "source .venv/bin/activate && streamlit run mcq-generator/StreamlitAPP.py --server.port $PORT --server.headless true --server.enableCORS false --server.enableXsrfProtection false"];
          manager = "web";
        };
      };
    };
  };
}
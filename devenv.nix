{ pkgs, config, ... }:

{
  # devenv debug mode
  devenv.debug = false;

  # environment variables
  env.ENVIRONMENT="tst";
  env.AWS_ACCOUNT="783648717275";  # s-ab01-foobar-tst
  env.DEBUG="True";
  env.GREET = "---->> hello! ready to code?";
  env.VERSIONS = "---->> versions";

  # cross-shell prompt
  starship = {
    enable = true;
    config.enable = true;
    config.path = "${config.env.DEVENV_ROOT}/starship.toml";
  };

  # language support
  languages.python = {
    enable = true;
    version = "3.10";
    poetry.enable = true;
    poetry.activate.enable = true;
    poetry.install.enable = true;
  };
  languages.javascript = {
    enable = true;
    npm.install.enable = true;
    package = pkgs.nodejs_18;
  };

  # devenv packages
  packages = [
      pkgs.nodejs_18
      pkgs.python310Packages.pip
    ];

  # hello script
  scripts.hello.exec = "echo $GREET";

  # echo versions
  scripts.versions.exec = "
    echo $VERSIONS
    echo
    git --version
    python --version
    poetry --version
    echo pip $(pip --version | cut -d ' ' -f2)
    echo nodejs $(node --version | cut -d 'v' -f2)
    echo npm $(npm --version)
    echo aws-cdk $(npm run -- cdk --version)
  ";

  # enter devenv shell
  enterShell = ''
    echo
    versions
    echo
    hello
  '';

  # See full devenv reference at https://devenv.sh/reference/options/
}
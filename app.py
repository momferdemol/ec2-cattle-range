#!/usr/bin/env python3

from aws_cdk import App

from cattle_range.settings import (
    get_settings,
    get_stack_name,
    print_settings,
    set_environment,
)
from cattle_range.stack import Range

app = App()

stack = Range(
    app,
    get_stack_name(""),
    description="Cattle range infra",
    env=set_environment("eu"),
    termination_protection=False,
)

if get_settings().debug:
    print_settings()

app.synth()

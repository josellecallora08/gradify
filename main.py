import asyncio
import json
import os
import argparse
from typing import Dict
from app.common import AppContext, Worker
from app.src.handlers import EvaluateRealization, EvaluateTrainees, ContentGenerator
from app.config.setup_context import context
from app.interfaces import CallbackHandler
from app.enums import AssessmentType
from app.config.initialize_dependencies import initialize_dependencies

Handlers = Dict[str, CallbackHandler]

async def main(
        server_task: AssessmentType,
        ctx: AppContext,
        worker: Worker,
        handlers: Handlers
):
    
    should_exit = False

    await worker.sync()

    ctx.logger.info('queue count: %s', ctx.task_queue.remaining())

    while not should_exit:
        try:
            if not ctx.task_queue.is_empty():
                ctx.logger.info('queue count: %s', ctx.task_queue.remaining())
                task = ctx.task_queue.pop()
                payload = task.payload
                assessment_type = task.type

                if(assessment_type == server_task):
                    await handlers[assessment_type].handler(payload)
            else:
                await worker.sync()
        except KeyboardInterrupt:
            should_exit = True


if __name__ == "__main__":
    print("starting...")
    parser = argparse.ArgumentParser(description='OkPo x Trainees Background processor')
    parser.add_argument(
        '--server-task',
        type=str,
        default='cg',
        choices=['er', 'et', 'cg'],
        help='Choose which task to run'
    )

    args = parser.parse_args()

    task_map = {
        "er": AssessmentType.EVALUATE_REALIZATION,
        "et": AssessmentType.EVALUATE_TRAINEES,
        "cg": AssessmentType.CONTENT_GENERATOR
    }

    # map shortcut name to its real name
    server_task = task_map[args.server_task]

    print("Server task:", server_task)

    initialize_dependencies()

    # map handlers for all supported assessments
    handlers: Handlers = {
        AssessmentType.EVALUATE_REALIZATION: EvaluateRealization(context),
        AssessmentType.EVALUATE_TRAINEES: EvaluateTrainees(context),
        AssessmentType.CONTENT_GENERATOR: ContentGenerator(context)
    }

    worker = Worker(context, server_task)

    asyncio.run(main(server_task, context, worker, handlers))
                
# class Main:
#     def __init__(self, ctx: AppContext):
#         self.ctx = ctx
#         self.evaluate_realization = EvaluateRealization(self.ctx)

#     def run(self):

#         self.evaluate_realization.handler()  # ✅ CALL the handler
#         self.ctx.logger.info("Application finished.")

# if __name__ == "__main__":
#     app = Main(ctx=context)
#     app.run()

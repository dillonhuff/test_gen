from itertools import chain

from cpp_code import *

class Task():
    def __init__(self, name, region_requirements):
        self.name = name
        self.logical_regions_created = []
        self.region_requirements = region_requirements
        self.child_tasks = []

    def all_field_spaces(self):
        return map(lambda rr: rr.region.field_space, self.region_requirements)

    def collect_field_spaces(self):
        all_field_spaces = map(lambda lr: lr.field_space, self.logical_regions_created)
        for child in self.child_tasks:
            all_field_spaces += child.collect_field_spaces()
        return all_field_spaces

    def collect_tasks(self):
        all_tasks = [self]
        for child in self.child_tasks:
            all_tasks += child.collect_tasks()
        return all_tasks        

    def index_spaces_init(self):
        index_spaces = map(lambda x: x.index_space, self.logical_regions_created)
        index_spaces_to_init = filter(lambda i: i.task_name == self.name, index_spaces)
        return list(chain(*map(lambda i: i.init_code(), index_spaces_to_init)))

    def field_spaces_init(self):
        field_spaces = map(lambda x: x.field_space, self.logical_regions_created)
        field_spaces_to_init = filter(lambda fs: fs.task_name == self.name, field_spaces)
        init_code_lists = map(lambda fs: fs.init_code(), field_spaces_to_init)
        init_code = []
        for i in init_code_lists:
            init_code.extend(i)
        return init_code

    def logical_regions_created_init(self):
        return list(chain(*map(lambda lr: lr.init_code(self.name), self.logical_regions_created)))

    def logical_regions_init(self):
        return self.index_spaces_init() + self.field_spaces_init() + self.logical_regions_created_init()

    def region_requirements_code(self, launcher_name):
        rr_code = []
        i = 0
        for rr in self.region_requirements:
            rr_code.extend(rr.init_code(i, launcher_name))
            i += 1
        return rr_code

    def launch_code(self):
        launcher_name = self.name + '_launcher'
        null_arg = cpp_var('TaskArgument(NULL, 0)')
        launcher_init = cpp_funcall('TaskLauncher ' + launcher_name, [], [self.id(), null_arg])
        launch_call = cpp_funcall('runtime->execute_task', [], ['ctx', launcher_name])
        return [launcher_init] + self.region_requirements_code(launcher_name) + [launch_call]

    def child_task_launches(self):
        launches = []
        for child_task in self.child_tasks:
            launches.extend(child_task.launch_code())
        return launches
    
    def task_function(self):
        task_body = self.logical_regions_init() + self.child_task_launches()
        return cpp_function(cpp_void(), self.name, [], task_args, task_body)

    def registration_code(self):
        args = [cpp_var(self.id()),
                cpp_var("Processor::LOC_PROC"),
                cpp_var("true"),
                cpp_var("false")]
        return cpp_funcall("HighLevelRuntime::register_legion_task", [self.name], args)

    def id(self):
        return self.name.upper() + "_ID"

    def should_print_region_requirements(self):
        map(lambda rr: rr.should_print(), self.region_requirements)

    def should_print_regions_created(self):
        map(lambda lr: lr.should_print_if_any_child_is_needed(), self.logical_regions_created)

    def decide_what_should_print(self):
        all_tasks = self.collect_tasks()
        map(lambda t: t.should_print_region_requirements(), all_tasks)
        map(lambda t: t.should_print_regions_created(), all_tasks)

    def shouldnt_print_regions(self):
        map(lambda lr: lr.shouldnt_print_anything(), self.logical_regions_created)

    def shouldnt_print_anything(self):
        map(lambda t: t.shouldnt_print_regions(), self.collect_tasks())

# Task argument boilerplate
runtime = cpp_formal_param(cpp_ptr(cpp_var("HighLevelRuntime")), cpp_var("runtime"))
context = cpp_formal_param(cpp_var("Context"), cpp_var("ctx"))
regions = cpp_formal_param(cpp_const(cpp_ref(cpp_var("std::vector<PhysicalRegion>"))), cpp_var("regions"))
task = cpp_formal_param(cpp_const(cpp_ptr(cpp_var("Task"))), cpp_var("task"))
task_args = [task, regions, context, runtime]

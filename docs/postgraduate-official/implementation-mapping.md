# ربط المرجع الرسمي بهندسة المنصة

تاريخ المرجع: **2026-09-08**

هذا الملف يحول القواعد والبيانات الرسمية المجمعة إلى متطلبات تصميم للمنصة. الهدف هو منع تحويل اللوائح إلى شروط ثابتة داخل Django/React، وضمان أن نفس المحرك يعمل لاحقاً لكلية أخرى أو جامعة أخرى.

## 1) الهيكل المؤسسي والأكاديمي

الكيانات الأساسية:

`University → Faculty → Department → Program → AcademicDegree`

مع إضافة طبقة قانونية/زمنية مستقلة:

`Program → ProgramApproval → RegulationVersion`

### لماذا؟

الكتالوج الرسمي لكلية الطب يحتوي 33 صفاً أكاديمياً، لكن الهيكل التنظيمي الحالي للأقسام قد يتطور بمرور الوقت، كما أن بعض البرامج منشورة مع انتظار القرار الوزاري. لذلك:

- `Department` يمثل القسم التنظيمي الحالي.
- `Program` يمثل البرنامج الذي يمنح درجة محددة.
- `ProgramApproval` يمثل حالة الاعتماد ومرجعه.
- `RegulationVersion` يمثل نسخة اللائحة وفترة سريانها.

لا يجوز استنتاج أن كل قسم لديه ماجستير ودكتوراه تلقائياً.

## 2) الطالب والتاريخ الأكاديمي

`Student` يمثل هوية الشخص الدائمة فقط.

كل مرحلة دراسية تُسجل في:

`AcademicEnrollment`

وبالتالي يمكن للطالب أن يكون له:

`Diploma Enrollment → Master Enrollment → Doctorate Enrollment`

دون فقد أي مرحلة سابقة.

الحقول الأساسية المقترحة للقيد:

- `student`
- `program`
- `regulation_version`
- `academic_year`
- `admission_cycle`
- `enrollment_date`
- `status`
- `completion_date`
- `cancellation_reason`
- `decision_reference`
- `effective_from/effective_to`

كل تغيير حالة ينشئ `AcademicEnrollmentEvent` بدلاً من تعديل التاريخ بصمت.

## 3) حالات القيد

لا تُحذف سجلات القيد الملغاة أو المنتهية. الحالات يجب أن تكون قابلة للتهيئة، مع مجموعة أولية مثل:

- `PENDING_DOCUMENTS`
- `UNDER_DEPARTMENT_REVIEW`
- `UNDER_FACULTY_REVIEW`
- `APPROVED`
- `ACTIVE`
- `SUSPENDED`
- `CANCELLED_BY_REQUEST`
- `CANCELLED_ABSENCE`
- `COMPLETED`
- `DEGREE_AWARDED`

الأسماء والمسارات النهائية يجب أن تأتي من Workflow Configuration، لا من if/else ثابتة لكل كلية.

## 4) شروط القبول

الكيانات المقترحة:

- `AdmissionRule`
- `AdmissionRequirement`
- `AdmissionCycle`
- `ProgramCapacity`

كل قاعدة تحمل:

- الجهة/الكلية/البرنامج/الدرجة التي تنطبق عليها.
- نسخة اللائحة.
- تاريخ البداية والنهاية.
- نوع الشرط.
- القيمة أو الصيغة.
- هل هي إلزامية أم قابلة للاستثناء.
- جهة اعتماد الاستثناء.

مثال: شرط تقدير الماجستير لا يُكتب `if GPA >= GOOD` داخل الكود؛ يُخزن كقاعدة مرتبطة بنسخة اللائحة.

## 5) مستندات القيد

الكيانات:

- `DocumentType`
- `ProgramDocumentRequirement`
- `EnrollmentDocument`
- `DocumentVerification`

يجب دعم اختلاف المستندات حسب:

- الدرجة.
- مصري/وافد.
- عامل/غير عامل.
- موقف التجنيد.
- البرنامج واللائحة.

## 6) المنهج والمقررات والامتحانات

الكيانات:

- `CurriculumVersion`
- `ProgramStage`
- `Course`
- `ProgramCourseRequirement`
- `ExamSession`
- `ExamAttempt`
- `Result`

وذلك لدعم أجزاء الماجستير والدكتوراه، المقررات الإجبارية والاختيارية، الامتحان التأهيلي، وتغير المناهج مع اللوائح.

## 7) تسجيل البحث والرسالة

المسار الصحيح:

`AcademicEnrollment → ResearchProtocol → Thesis`

وليس:

`Student → Thesis`

لأن نفس الطالب يمكن أن تكون له رسالة ماجستير ورسالة دكتوراه.

الكيانات المقترحة:

- `ResearchProtocol`
- `ResearchRegistrationRequirement`
- `ResearchRequirementEvidence`
- `Thesis`
- `ThesisStatusEvent`

ومن متطلبات التسجيل التي يجب دعم إثباتها: حساب المكتبة الرقمية/قواعد البيانات وبنك المعرفة وفق القرارات الرسمية المسجلة في المرجع.

## 8) الإشراف

الكيانات:

- `ThesisSupervisor`
- `SupervisorRole`
- `SupervisionAppointment`
- `SupervisionChangeEvent`
- `SupervisionCapacityRule`

يجب حفظ القسم والجهة والدرجة العلمية والصفة، وقرار التعيين والتغيير، وليس أسماء المشرفين كنصوص فقط.

## 9) النشر العلمي

الكيانات:

- `PublicationRequirement`
- `ResearchPublication`
- `PublicationIndexingEvidence`
- `PublicationVerification`

الحقول تشمل:

- title
- DOI
- journal
- publication_date
- indexing database
- impact factor / promotion score عند الحاجة
- verification office
- verified_by / verified_at
- regulation rule used

شرط النشر للماجستير والدكتوراه مختلف، وقد يتغير، لذلك يرتبط بالدرجة والبرنامج ونسخة اللائحة.

## 10) لجنة الحكم والمناقشة

`DefenseCommittee` لا يكفي أن يحتوي على تاريخ المناقشة فقط.

الكيانات المقترحة:

- `DefenseCommittee`
- `CommitteeMember`
- `CommitteeNomination`
- `CommitteeApproval`
- `ExaminerReport`
- `DefenseResult`
- `DefenseScheduleEvent`

يجب أن يستطيع Rule Engine التحقق من:

- عدد الأعضاء.
- وجود المشرف.
- الأستاذ الأقدم/رئيس اللجنة.
- العضو الخارجي حسب الدرجة.
- جهة كل محكم.
- مدة صلاحية التشكيل.
- تضارب المصالح/صلة القرابة عندما تنطبق القاعدة.

## 11) مدة القيد والتنبيهات

الحدود الرسمية المؤرخة مثل 6 سنوات للماجستير و8 سنوات للدكتوراه يجب أن تمثل في:

`EnrollmentDurationRule`

مع:

- minimum duration
- maximum duration
- extension rule
- effective dates

وتنشئ المنصة تنبيهات قبل انتهاء الحدود بدلاً من انتظار المخالفة.

## 12) اللغة

`LanguageRequirement`

يحتوي على:

- test type
- minimum score
- equivalency
- applies_to degree/program
- must_complete_before stage
- effective dates

لا يُثبت TOEFL/ELPT كقيمة واحدة لكل الجامعات.

## 13) منح الدرجة

الكيانات:

- `DegreeRequirement`
- `RequirementCompletion`
- `DegreeAwardRequest`
- `DegreeAwardDecision`

لا يتم تغيير الطالب إلى `GRADUATED` بمجرد انتهاء المناقشة. يجب أن يستطيع النظام التحقق من جميع متطلبات اللائحة الفعالة وقت قيد الطالب.

## 14) Workflow والسلطات

القواعد الرسمية تشير إلى أدوار مجلس القسم، لجنة الدراسات العليا، مجلس الكلية، وسلطات الجامعة. التنفيذ يجب أن يعتمد على:

- `WorkflowDefinition`
- `WorkflowStep`
- `WorkflowTransition`
- `RequiredRole/Permission`
- `ApprovalAction`

مع Audit Trail كامل.

التفويضات أو اختلاف المسار بين كلية وأخرى تكون Configuration وليست تعديل كود.

## 15) البرامج المهنية وحالة الاعتماد

الحد الأدنى لحالة البرنامج:

- catalog status
- operational status
- legal approval status
- decision number/date
- source/evidence
- effective dates

وجود إعلان فتح باب التقديم أو نتيجة امتحان يثبت نشاطاً تشغيلياً، لكنه لا يحل محل توثيق قرار الاعتماد عند الحاجة.

## 16) Dashboard مدير البرنامج

الداشبورد يجب أن يقرأ من البيانات أعلاه، لا من counters ثابتة. التبويبات الرئيسية المطلوبة:

- الأقسام العلمية.
- الدبلومات.
- الماجستير.
- الدكتوراه.
- الطلاب وسجلهم الأكاديمي.
- التسجيلات والطلبات.
- الرسائل والبروتوكولات.
- الإشراف.
- اللجان والمناقشات.
- النشر ومتطلبات المنح.
- التقارير والتنبيهات.
- إدارة البرامج واللوائح والصلاحيات.

إضافة/إخفاء/ترتيب هذه الوحدات يجب أن تتم من Platform Administration وليس بتعديل `main.jsx`.

## 17) Dashboard وكيل الكلية

نفس البيانات والمحرك، لكن View وصلاحيات مختلفة. أمثلة مؤشرات:

- الطلاب حسب الدرجة والقسم.
- طلبات تحتاج اعتماداً.
- حالات قرب تجاوز مدة القيد.
- الرسائل المتوقفة.
- اللجان المنتظرة للاعتماد.
- المناقشات القادمة.
- استيفاء النشر ومتطلبات المنح.
- أداء الأقسام والبرامج.

لا يُبنى Dashboard مستقل بنسخة Business Logic مكررة؛ الفرق يكون Role + Permissions + Dashboard Configuration.

## 18) قاعدة التوسع للجامعات الأخرى

أي كيان تنظيمي أو قاعدة قابلة للاختلاف يجب أن يكون Scoped:

`Institution/University → Faculty → Department/Program → RegulationVersion`

ولا تُستخدم أسماء «كلية الطب جامعة أسيوط» داخل Business Logic. بيانات الهوية Branding والإدارة والشعار والألوان تُدار من إعدادات المؤسسة.

## ترتيب التنفيذ المقترح

1. تثبيت `AcademicEnrollment` + history بصورة كاملة.
2. إضافة `RegulationVersion` و`ProgramApproval`.
3. استيراد كتالوج البرامج الرسمي من `academic-programs.json` مع مراجعة إدارية قبل التفعيل.
4. بناء Document Requirements وAdmission Rules.
5. نقل `Thesis` تدريجياً من `Student` إلى `AcademicEnrollment` مع Migration آمنة.
6. تطوير supervision + committee members + publication requirements.
7. بناء dashboards ديناميكية للأقسام/الدبلومات/الماجستير/الدكتوراه.
8. بناء Platform Administration لتغيير البرامج والقوائم والصلاحيات والهوية والـworkflows بدون تعديل الكود.

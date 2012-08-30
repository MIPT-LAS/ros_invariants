
(in-package :asdf)

(defsystem "invariants-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :roslib-msg
)
  :components ((:file "_package")
    (:file "InvariantStatus" :depends-on ("_package"))
    (:file "_package_InvariantStatus" :depends-on ("_package"))
    ))

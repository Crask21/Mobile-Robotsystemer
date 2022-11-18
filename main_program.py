from DTMF.DTMF_overclass import DTMF

robot=DTMF(10)
robot.listen.startListen()
pack=robot.send.rand_pack(10)

robot.send.send_package([*robot.send.synchroniazation(10),*pack])
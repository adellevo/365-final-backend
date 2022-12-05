from project import OracleClient
from project.models import Oracle
from . import scheduler,db,app

oc = OracleClient()


@scheduler.task('interval', id='oracle_manager', seconds=10, misfire_grace_time=900)
def oracle_update():
    with app.app_context():
        print("Running oracle manager")
        
        new_prices = oc.update_switchboard()
        for price in new_prices:
            print("PRICE",price)
            o = Oracle(
                oracleName=price[0]+"_switchboard",
                price=price[1],
                timestamp=price[2])

            # check if this oracle already exists
            oracle = Oracle.query.filter_by(oracleName=o.oracleName, timestamp=price[2]).first()
            if oracle is None:
                db.session.add(o)
            
        db.session.commit()
    # get all the stashes

import concurrent.futures
import threading

from .enums.user_tier import UserTier
from .model.user import User
from .service.rate_limiter_service import RateLimiterService


def check_concurrency(rate_limiter_service: RateLimiterService) -> None:
    free_user1 = User("user1", UserTier.FREE)

    threads = 20
    barrier = threading.Barrier(threads)
    remaining = threads
    remaining_lock = threading.Lock()
    latch_event = threading.Event()

    def count_down() -> None:
        nonlocal remaining
        with remaining_lock:
            remaining -= 1
            if remaining == 0:
                latch_event.set()

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        for i in range(1, threads + 1):
            req_num = i

            def task(req_num: int = req_num) -> None:
                try:
                    barrier.wait()
                except Exception:
                    import traceback

                    traceback.print_exc()

                allowed = rate_limiter_service.allow_request(free_user1)
                print(
                    f"{threading.current_thread().name} | Request {req_num} "
                    f"for FreeUser1: {'ALLOWED' if allowed else 'BLOCKED'}"
                )
                count_down()

            executor.submit(task)

        latch_event.wait()


def main() -> None:
    rate_limiter_service = RateLimiterService()

    # free_user = User("user1", UserTier.FREE)
    # premium_user = User("user2", UserTier.PREMIUM)

    check_concurrency(rate_limiter_service)


if __name__ == "__main__":
    main()

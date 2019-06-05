#ifndef __VERSION_H__
#define __VERSION_H__

/* This format follows the Semantic Versioning 2.0.0[https://semver.org/] specification. */

/* comment macro if don't append pre-release version or build metadata */
#define PRE_RELEASE		"release"
#define BUILD			"1559717577"

/* major minor patch */
#define VERSION_CORE    "1.0.0"

#if defined(VERSION_CORE)
#if  defined(PRE_RELEASE) && defined(BUILD)
#define SW_VESION VERSION_CORE"-"PRE_RELEASE"+"BUILD
#elif defined(PRE_RELEASE)
#define SW_VESION VERSION_CORE"-"PRE_RELEASE
#elif defined(BUILD)
#define SW_VESION VERSION_CORE"+"BUILD
#else
#define SW_VESION VERSION_CORE
#endif
#else
#define SW_VESION
#error VERSION_CORE is not define!
#endif

#endif
